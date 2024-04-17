recording_ids = [
    '580704103_580704103_3001550406F0240401_01April2024_220436',
    '580842427_580842427_3001550519F0240401_01April2024_221246',
    '581333626_581333626_3001550311F0240401_01April2024_215933',
    '590691174_590691174_3001550281F0240401_01April2024_215802',
    '590691174_590691174_3001550466F0240401_01April2024_220741',
    '591602222_591602222_3001550590F0240401_01April2024_221607',
    '592285555_592285555_3001550309F0240401_01April2024_220048',
    '592877888_592877888_3001550340F0240401_01April2024_220229',
    '593180512_593180512_3001550231F0240401_01April2024_215508',
    '593825453_593825453_3001550654F0240401_01April2024_221750'
]

# Add single quotes around each RecordingId value
quoted_recording_ids = [f"'{recording_id}'" for recording_id in recording_ids]


print(quoted_recording_ids)
