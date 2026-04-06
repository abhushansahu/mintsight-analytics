# Changelog

All notable changes to this project are documented here. Dates use UTC.

## [Unreleased]

Board-facing copy aligned with this window: [docs/board-narrative.md](docs/board-narrative.md).

### Added

- Frontend: top navigation across Overview, Entities, Categories, and Flows.
- App routes: `/entities`, `/entities/[slug]`, `/categories`, `/categories/[category]`, `/flows`, `/flows/[commerceType]`.
- `useUrlSelectors` hook for URL-synced dashboard filters.

### Changed

- Frontend production build runs with `cross-env NODE_ENV=production` for consistent behavior across environments.
