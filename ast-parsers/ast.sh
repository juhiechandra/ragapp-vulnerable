#!/bin/bash

FILE="$1"
EXT="${FILE##*.}"

# Get the base filename without path and extension
BASENAME=$(basename "$FILE" ".$EXT")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR"

if [ "$EXT" = "py" ]; then
    OUTPUT_FILE="$OUTPUT_DIR/${BASENAME}.ast"
    python3 -c "
import ast, json, sys
with open('$FILE') as f:
    tree = ast.parse(f.read())
ast_output = ast.dump(tree, indent=2)
with open('$OUTPUT_FILE', 'w') as out:
    out.write(ast_output)
print(ast_output)
"
elif [ "$EXT" = "js" ]; then
    OUTPUT_FILE="$OUTPUT_DIR/${BASENAME}.json"
    npx acorn --ecma2020 "$FILE" | npx json > "$OUTPUT_FILE"
    cat "$OUTPUT_FILE"
else
    echo "Unsupported file type: $EXT"
    exit 1
fi

echo ""
echo "AST graph saved to: $OUTPUT_FILE"