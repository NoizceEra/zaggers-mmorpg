# High realms build notes

- Regenerator: `scripts/build_high_realms.py` (`build_remaining_realms.py` wraps it).
- Monster shape matches meadows: string ids, `sprite` with `_ff` suffix, `rank` only on elite/rare/boss.
- Boss HP locked to BESTIARY curve: Vashkar 10644, Sylveth 14980, Verrocaine 20928.
- Rootways defaultTile kept as `tile_dungeon_rune` to match DB; painted tiles use root set.
- Spire↔Rootways exit is on Collapsed Skybridge (-26,20), not the Crown.
- Chasm↔Rootways exit is at Thronehall (0,30).
- No town portal on rootways (verified).
