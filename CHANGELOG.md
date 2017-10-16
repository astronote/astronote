# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [0.3.0]
### Added
- Version comparisons to the bottom of the changelog.
- EditorConfig file.
- `get_solstice_type` and `get_equinox_type` methods.
- `is_date` method to check if a variable is an instance of `ephem.Date`.

### Removed
- The `get_moon_phase` method as it was only ever called once.
- All methods and references to calculating twilight times, including planet
  visibility methods.

### Changed
- The structure of files, opting to group related methods into modules which are
  imported into the core module.
- The structure of tests to match the file changes.
- Some test cases to focus less on the value and more on the correct type being
  returned instead; this is due to tests constantly failing because of
  imprecise number, etc.
- Changed lunar methods:
  - `get_major_moon_phase` to `is_major_phase`.
  - `is_moon_apogee` to `is_at_apogee`.
  - `is_moon_perigee` to `is_at_perigee`.

### Fixed
- The `if` statement in `get_meteor_showers` that was cancelling early; the
  logic had to be adjusted.


## [0.2.0]
### Added
- A changelog.
- A start argument to the following methods in order to get the next occurrence
  of that event from a specific date and time:
  - `get_next_rise`;
  - `get_next_set`;
  - `get_twilight_start`; and
  - `get_twilight_end`.
- A check for planet visibility based on the planet's closeness to the Sun.
- A check for separations to be no more than 4 degrees apart to be listed as an
  event.
- A validation check for elongations so that false positives were not being
  returned when an inferior planet's elongation crossed from a negative value to
  a positive.

### Changed
- Improved the accuracy of the planet visibility flags.

### Fixed
- Word wrapping in the license.

## [0.1.0]
### Added
- The foundational functions of AstroNote as one initial commit.


[Unreleased] https://github.com/dfranklinau/astronote/compare/v0.3.0...HEAD
[0.3.0] https://github.com/dfranklinau/astronote/compare/v0.2.0...v0.3.0
[0.2.0] https://github.com/dfranklinau/astronote/compare/v0.1.0...v0.2.0
