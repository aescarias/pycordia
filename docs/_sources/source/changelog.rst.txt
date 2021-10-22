Changelog
=========    

0.2.0 ('pre-alpha'; The First Big Step)
---------------------------------------

- Functions added in `utils`: `utils.mutually_exclusive`, `utils.snowflake_to_date`, `utils.make_optional`
- Improved `GatewayError`, added `MutuallyExclusiveError`
- `Client` now supports multiple handlers for same event
- Added `api.request` function that all models use
- All models no longer require a `Client` object as first argument
- `RoleTags` and `Emoji` have been moved to `models/guild.py`
- `User` model: Renamed `User.user_from_id` to `User.from_id`
- `Message` model: `Message.create` merged with `Message.send`
- `Message` model: Renamed `Message.get_message` to `Message.from_id` 
- Added `Guild` model
- `Channel` model: Renamed `Channel.query_message` to `Channel.get_message`
- `Channel` model: Added `Channel.get_messages` and `Channel.get_pinned_messages`



