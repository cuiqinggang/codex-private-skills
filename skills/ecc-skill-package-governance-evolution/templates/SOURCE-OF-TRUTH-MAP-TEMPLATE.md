# Source Of Truth Map Template

## purpose

Create a map that tells agents which file owns each rule.

## inputs

- root file list
- templates list
- prompts list
- existing policies

## forbidden scope

- duplicating full rules into every file
- conflicting authorities

## gates

1. list topics
2. assign primary source
3. assign supporting files
4. define conflict rule
5. verify references

## required evidence

- topic table
- conflict rule
- reference check

## script verification

Check required source files exist and are referenced.

## final status codes

- ECC_SOURCE_OF_TRUTH_MAP_PASS

## failure status codes

- ECC_SOURCE_OF_TRUTH_MAP_STOP
