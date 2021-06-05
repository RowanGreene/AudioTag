# AudioTag
A Python command line that uses [Mutagen](https://github.com/quodlibet/mutagen)
to edit metadata tags in audo files.

## Supported formats
Currently, AudioTag only handles FLAC and Ogg Vorbis files. Support for other
formats supported by Mutagen, including MP3, MP4, and WAVE, is pending.

## Dependencies
AudioTag requires Python3.6+, as well as an installation of Mutagen.

## Using AudioTag
* First, clone the repository into a local directory:
```
git clone https://github.com/RowanGreene/AudioTag
```
* Next, run AudioTag with the name of the file you want to edit:
```
./audiotag.py file.flac
```
* For information on commands accepted by AudioTag, run `help`.
* When you're done editing the file's tags, `save` your work and `quit`.

## Licensing
AudioTag is licensed under the [GPL](LICENSE) version 3 or later.
