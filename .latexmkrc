# latexmk 配置：XeLaTeX + BibTeX 链路
# 本文档依赖 newtxtext/newtxmath 与 microtype(protrusion)，须用 XeLaTeX 编译；
# 参考文献由 \bibliography{c-back-matter/references} + IEEEtran 样式经 BibTeX 处理。

$pdf_mode = 5;   # 5 = 使用 xelatex 直接生成 PDF
$postscript_mode = 0;
$dvi_mode = 0;

$xelatex = 'xelatex -synctex=1 -shell-escape=0 -interaction=nonstopmode -halt-on-error -file-line-error %O %S';

# 2 = 始终运行 bibtex，且 latexmk -C 时清理 .bbl
$bibtex_use = 2;
$bibtex = 'bibtex %O %B';

# 章节分散在子目录，确保 latexmk 能追踪 .aux 依赖
$recorder = 1;
$max_repeat = 6;

# 输出目录为 build/ 时，BibTeX/XeLaTeX 的工作目录会变化，
# 需显式把源码目录及其子目录加入搜索路径，否则找不到 references.bib 与 assets/ 图片。
$ENV{'BIBINPUTS'} = '.:./c-back-matter:' . ($ENV{'BIBINPUTS'} // '');
$ENV{'TEXINPUTS'} = '.:./assets:./c-front-matter:./c-back-matter:' . ($ENV{'TEXINPUTS'} // '');

# 输出集中到 build/，保持源码目录干净
$out_dir = 'build';
$aux_dir = 'build';

# 需要一并清理的中间文件
$clean_ext = 'synctex.gz run.xml bbl bcf fls fdb_latexmk lof lot toc out';

# 编译成功后归档一份带时间戳的 PDF 到 build/archive/，
# build/main.pdf 本身保持固定路径不变，实时预览才不会断链。
# 设 LATEXMK_ARCHIVE_KEEP=0 可关闭数量清理；不想归档就注释掉下一行。
$success_cmd = 'tools/archive-pdf.sh %D';

# -pvc 模式下的预览器（本机未装 Skim，用系统「预览」；装了 Skim 可换成 -a Skim 以获得自动重载）
$pdf_previewer = 'open -a Preview';
$pdf_update_method = 4;
$pdf_update_command = 'open -a Preview %S';
