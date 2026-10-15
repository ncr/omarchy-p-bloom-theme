"""Keep the active p(bloom) desktop matched to connected monitors."""
import argparse
import os
from pathlib import Path
import sys
import time
import wallpaper_profiles as wp


def stamp(path):
    try:
        s=path.stat()
        return (s.st_ino,s.st_mtime_ns,s.st_size)
    except OSError:
        return None


def fingerprint(root,screens):
    # Focus, window moves and wallpaper cycling do not require recopying assets.
    topology=sorted((m['name'],m['width'],m['height'],m['scale']) for m in screens)
    current=wp.current_dir()
    return (topology,stamp(current/'theme.name'),stamp(current/'theme'),
            stamp(root/'docs/collection/profiles.json'),stamp(wp.setup_path()))


class DesktopWatcher:
    def __init__(self,root):
        self.root=root
        self.last=None
        self.retry_at=None

    def tick(self):
        screens=wp.monitors()
        if not screens or not wp.active_theme(wp.current_dir()):
            self.last=None
            return False
        signature=fingerprint(self.root,screens)
        if signature==self.last and not (self.retry_at and time.time()>=self.retry_at):
            return False
        previous=wp.read_setup()
        requested=previous.get('profile','auto') if previous.get('version')==6 and previous.get('root')==str(self.root) else 'auto'
        monitor=previous.get('monitor')
        if monitor not in {m['name'] for m in screens}:monitor=None
        _,available=wp.profiles(self.root)
        if requested not in {'auto',*(p['id'] for p in available)}:requested='auto'
        p=wp.plan(self.root,requested,monitor,screens,level=wp.saved_level(previous,self.root))
        result=wp.initialize(self.root,p,requested,monitor)
        # Offline or a failed download: the installed set stays; try again later.
        self.retry_at=time.time()+wp.RETRY_SECONDS if result and result.get('fallback') else None
        # Synchronization itself touches the stage and preferences.
        self.last=fingerprint(self.root,screens)
        return True


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args()
    watcher=DesktopWatcher(args.root.resolve())
    last_error=None
    gone=None
    while True:
        # Omarchy's Remove > Theme deletes the theme's folder: once it has been gone for a minute (a reinstall clones
        # it back within seconds), the app removes itself, its downloads and settings with it, and stops
        if not args.root.is_dir():
            gone=gone or time.time()
            if time.time()-gone>=60:
                import wallpaper_uninstall
                wallpaper_uninstall.remove(Path(__file__).resolve().parents[2],purge=True,from_service=True)
                wallpaper_uninstall.notify('p(bloom) Wallpapers removed','The p(bloom) theme was removed, so its app and downloaded wallpapers went with it.')
                return
            time.sleep(10)
            continue
        gone=None
        # `omarchy theme update` pulls the checkout; the installed copy of the app follows it, then restarts
        app=Path(__file__).resolve().parent
        if app!=args.root.resolve()/'tools':
            import wallpaper_runtime
            try:
                if wallpaper_runtime.refresh(app,args.root):
                    os.execv(sys.executable,[sys.executable,str(app/'wallpaper_desktop.py'),*sys.argv[1:]])
            except OSError as exc:
                print(f'p(bloom) app update failed: {exc}',file=sys.stderr,flush=True)
        try:
            watcher.tick()
            last_error=None
        except (OSError,ValueError,wp.subprocess.SubprocessError) as exc:
            if str(exc)!=last_error:
                print(f'p(bloom) desktop: {exc}',file=sys.stderr,flush=True)
                last_error=str(exc)
        time.sleep(10)


if __name__=='__main__':main()
