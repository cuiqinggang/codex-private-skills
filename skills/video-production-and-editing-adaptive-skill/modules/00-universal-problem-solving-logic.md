# Universal Problem-Solving Logic

Use this before choosing tools.

## Mature-Route Selection

For any video-related task, ask internally:

1. What final result does the user want?
2. What exact assets were provided?
3. Is this production, editing, trimming, repair, music, subtitles, or export?
4. Has a local workflow already succeeded for this class of task?
5. Which existing skill package should be reused?
6. What is the smallest tool path that can complete it?
7. What visible evidence will prove it worked?

## Anti-Pattern

Do not start like this:

```text
FFmpeg / Whisper / MoviePy / PySceneDetect / OpenCV / Computer Use / Jianying / PR
```

Then force the task into those tools.

## Correct Pattern

Start like this:

```text
goal -> assets -> mature workflow -> local adaptation -> minimum tool -> execute -> verify -> remember
```

## Risk Levels

- Low risk:
  read files, probe media, extract preview frames, create new outputs.
- Medium risk:
  create or update a skill/reference, batch render new files, generate reports.
- Stop and ask:
  delete source files, overwrite accepted files, modify account/system/security
  state, install large tools, or run unclear destructive operations.

## Completion Standard

The task is not complete until the user has:

- a usable output path
- a short explanation of what changed
- a verification result
- any important caveat, such as compatibility or skipped visual review
