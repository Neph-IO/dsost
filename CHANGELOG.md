# Changelog


## [1.0.0] - 2024-11-08
- After a bit of testing i think i'm ready for a 1.0 it look stable enough
- Formating to be ready to host on flathub

## [0.7.0] - 2024-11-07
- First Flatpak build Done
- Finishing removing VLC references
- Prepared the project to be FLATPACK Compatible (Flatpak-pip-generator)
- Check if the project runs on Host or Flatpak to define path
- Cleaned some useless comented code
- Fix End of stream event by starting another song.
- Fixed naming for flatpak packaging

## [0.6.0] - 2024-11-06
- Completely remove python-vlc from the project it's not usefull to have it installed
- Migrated the project to Gstreamer to handle the streaming process
- Reworked the UI to look better i think, i can't try on 4k screen so it might be to small on them
- Cleaned some useless comented code
- reworked the icon to have rounded angles (more icon'ish)


## [0.5.0] - 2024-11-04
- Reorganisation of the project in /data and /src, it looks like best practice
- Configuration of the project flatpak ready
- Cleaning some useless comment and old code
- Fucked up my Gitpush so redoing it

## [0.4.0] - 2024-11-03
- UI impovement (now i feel like showing it to my mom)
- add favicon

## [0.3.0] - 2024-11-03
- Updating the UI to be smaller and more aligned with itself
- changed button to be icons
- Changed changlog order
- Added Dark souls 2 Playlist
- Added Dark Souls 3 Playlist

## [0.2.1] - 2024-11-03
- separated Ui to another file becauces it looks cleaner this way
- Dark souls 1 playlist done.

## [0.2.0] - 2024-11-02
- Fix the randomizer at the end of a song who refused to read another random from same playlist.
- Added this changelog :)
- Added a get random song button
- started populating the playlist
- Add version number
- Add VERSION FILE cuz it's easier to write here than the in spagetti code
- Fixed Pause button starting a new song even when data are in buffer.
- Changed interfaces to have 2 buttons closes to eachothers

## [0.1.0] - 2024-11-02
- Initial commit with the basic project structure.
- Added main features (under testing).
- Initial documentation (subject to changes).
