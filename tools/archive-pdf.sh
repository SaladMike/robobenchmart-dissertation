#!/bin/bash
# 编译成功后归档一份带时间戳的 PDF 副本。
# 由 .latexmkrc 的 $success_cmd 调用，参数 $1 为刚生成的 PDF 路径。
#
# 设计取舍：
#   - build/main.pdf 始终保持固定路径，供 LaTeX Workshop / Skim 实时预览。
#   - 归档副本放在 build/archive/，文件名含时间戳，便于回溯比对。
#   - 自动只保留最近 KEEP 个副本，避免 21MB/次 迅速占满磁盘。

set -euo pipefail

SRC="${1:-}"

if [[ -z "$SRC" || ! -f "$SRC" ]]; then
    echo "[archive-pdf] 跳过：源文件不存在 ($SRC)" >&2
    exit 0
fi

# 归档目录固定在源 PDF 同级的 archive/ 下
ARCHIVE_DIR="$(cd "$(dirname "$SRC")" && pwd)/archive"
mkdir -p "$ARCHIVE_DIR"

BASE="$(basename "$SRC" .pdf)"
STAMP="$(date +%Y%m%d-%H%M%S)"
DEST="$ARCHIVE_DIR/${BASE}-${STAMP}.pdf"

# 内容未变则不重复归档，避免无意义的副本堆积
LATEST="$(ls -1t "$ARCHIVE_DIR/${BASE}"-*.pdf 2>/dev/null | head -1 || true)"
if [[ -n "$LATEST" ]] && cmp -s "$SRC" "$LATEST"; then
    echo "[archive-pdf] 内容与上次归档一致，跳过：$(basename "$LATEST")"
    exit 0
fi

cp -p "$SRC" "$DEST"
echo "[archive-pdf] 已归档 -> archive/$(basename "$DEST") ($(du -h "$DEST" | cut -f1))"

# 仅保留最近 KEEP 个副本
KEEP="${LATEXMK_ARCHIVE_KEEP:-10}"
if [[ "$KEEP" =~ ^[0-9]+$ ]] && [[ "$KEEP" -gt 0 ]]; then
    # shellcheck disable=SC2012
    ls -1t "$ARCHIVE_DIR/${BASE}"-*.pdf 2>/dev/null | tail -n "+$((KEEP + 1))" | while IFS= read -r old; do
        rm -f -- "$old"
        echo "[archive-pdf] 清理旧副本：$(basename "$old")"
    done
fi
