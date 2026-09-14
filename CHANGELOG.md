# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## v2.0.0 - 2026/09/15

### Added

- `Import` feature in the `Logs` menu.
- Feature to remove any row from the table in `Logs` menu.
- Pagination system in the `Logs` menu so that the pages don't get too long. At most 50 transactions can be in one page.

### Changed

- The whole codebase from Python to HTML, CSS, and JavaScript.
- The user interface. Not that huge of a difference.
- After pressing the `Record` button in the `Record` menu the app doesn't ask for confirmation anymore. It just alerts that the transaction is recorded.
- In the `Query` menu, the categories having amount zero are not displayed anymore.
- The monthly data shown in `Query` menu is defaulted to the earliest month available in the logs.
- All of the previously available settings from `Settings` menu are removed and replaced by the option of changing between `Light` and `Dark` themes.

### Removed

- `Save` feature from the `Logs` menu. The changes in the table are automatically saved now. Only clicking once on the target enables the editing mode.

### Fixed

- Adding the pagination system in `Logs` menu fixes the bug where the `Logs` menu screen turns blank.

## v1.1.1 - 2026/05/04

### Fixed

- The spill of the table in `Query` menu beyond the visible screen. Just made it scrollable.

## v1.1.0 - 2026/04/16

### Added

- `Query` menu, that shows aggregate (sum) monthly expense data.
- Feature to export logs as `logs.csv` file in user selected directory.
- Feature to save settings to `config.csv` file.
- Feature to export settings as `config.csv` file in user selected directory.

### Changed

- All pill-shaped button to rounded-rectangle-shaped.
- `Snacks` category to `Food`.
- Navigation bar icon style - outlined to standard.
- Increased font weight of the table header.
- Options on `Settings` menu.
- The layout in `Settings` menu.

### Removed

- `Quit` button from the `Record` menu.
