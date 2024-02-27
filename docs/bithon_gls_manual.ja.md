# NCBI のゲノムデータから最長代表配列を得る


## 最長代表配列？

1つのタンパク質コード遺伝子から転写される mRNA は選択的スプライシングによって
複数の転写産物 (スプライシングバリアント) を生成する。
([Modrek and Lee 2002](https://doi.org/10.1038/ng0102-13),
[Kelemen et al. 2013](https://doi.org/10.1016/j.gene.2012.07.083),
*etc.*)

NCBI にあがっている全タンパク質配列 (`protein.faa`) や
全 CDS 配列 (`cds_from_genomic.fna`) はスプライシングバリアントを含むため、
FASTA ファイル中の配列数は遺伝子数よりも多い。

スプライシングバリアントを含んだまま種々の解析を進めると、
遺伝子コピー数の過大評価などにつながるため、1遺伝子1転写産物 (代表配列) の形にすることも多い。

その方法の一つが各遺伝子の最長スプライシングバリアントを代表配列とすることであり、
`bithon gls` はこのための機能を提供する。


## NCBI からアクセッションでゲノムデータをダウンロードする

[`datasets`](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/)
コマンドや `curl` などによりアクセッションで `protein.faa` と `cds_from_genomic.fna` を
取得できる。 (もちろん全ゲノム配列 `genomic.fna` やアノテーションファイル `gff`, `gtf` も取得可能。)

```sh
## datasets の場合
datasets download genome accession GCF_016699485.2 --include cds,protein

## curl の場合
curl -OJ https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_016699485.2/download?include_annotation_type=CDS_FASTA,PROT_FASTA
```

ダウンロード後、`ncbi_dataset.zip` を解凍することで
`ncbi_dataset/data/_アクセッション_/` に各データを取得できる。


## `bithon gls` による最長配列の取得

See `bithon gls --help`, [`README.md`](https://github.com/ymat2/bithon/blob/main/README.md)

`bithon gls` の最も基本的な使い方は:

```sh
bithon gls -i ncbi_dataset/data/_アクセッション_ -o 出力先ディレクトリ
```

これにより `ncbi_dataset/data/_アクセッション_` の `protein.faa` と `cds_from_genomic.fna` から
最長配列を抜き出して `出力先ディレクトリ/` 下に `longest.pep.fa` および `longest.cds.fa` を生成する。


## 各引数の使い方

`-p`/`--prefix`
: `longest` の代わりのファイル名を指定。例えばアクセッションなど。

`--keep_identity`
: Partial sequence やタンパク質配列予測モデルの違いにより、
  しばしば `cds_from_genomic.fna` から翻訳される配列と `protein.faa` にはミスマッチが生じる。
  `--keep_identity` は [Standard codon table](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi)
  に従って CDS を翻訳し、`protein.faa` と一致するもののみを保持する。
  最長配列に mismatch がある場合も、mismatch がないもののなかで最長配列を選ぶ。
  したがってミトコンドリアにコードされた遺伝子を含む数十から数百遺伝子が欠損するため、
  遺伝子数を重視する解析の際には非推奨。

`--header`
: `original` または `gene` から選択。デフォルトは `original` で、もともとの転写産物の ID をそのままヘッダーにする。
  (例: `>XP_040503661.1`, `>NC_052532.1_cds_XP_040503661.1_1`)
  一方 `gene` は「遺伝子名_種名」をヘッダーとして採用する。
  (例: `>CARMIL3_Gallus_gallus`)

`--report`
: 必要に応じて、各転写産物ごとの情報を記載した TSV を出力する。内容は下記の通り:

| gene_id | protein_id | protein_length_aa | cds_id | cds_length_bp | identity | species |
| :--- | :--- | ---: | :--- | ---: | :--- | :--- |
| CARMIL3 | XP_040503661.1 | 1135 | NC_052532.1_cds_XP_040503661.1_1 | 3408 | True | Gallus_gallus |
| CARMIL3 | XP_040503669.1 | 1093 | NC_052532.1_cds_XP_040503669.1_2 | 3282 | True | Gallus_gallus |
| CARMIL3 | XP_040503651.1 | 1140 | NC_052532.1_cds_XP_040503651.1_3 | 3423 | True | Gallus_gallus |
| CARMIL3 | XP_040503649.1 | 1148 | NC_052532.1_cds_XP_040503649.1_4 | 3447 | True | Gallus_gallus |
| CARMIL3 | XP_040503637.1 | 1166 | NC_052532.1_cds_XP_040503637.1_5 | 3501 | True | Gallus_gallus |
| CARMIL3 | XP_040503664.1 | 1098 | NC_052532.1_cds_XP_040503664.1_6 | 3297 | True | Gallus_gallus |
| CARMIL3 | XP_040503643.1 | 1153 | NC_052532.1_cds_XP_040503643.1_7 | 3462 | True | Gallus_gallus |
| CARMIL3 | XP_040503634.1 | 1171 | NC_052532.1_cds_XP_040503634.1_8 | 3516 | True | Gallus_gallus |
| DHRS4 | NP_001264054.1 | 273 | NC_052532.1_cds_NP_001264054.1_9  | 822 | True | Gallus_gallus |
| DHRS4 | XP_046798619.1 | 228 | NC_052532.1_cds_XP_046798619.1_10 | 687 | True | Gallus_gallus |
| DHRS4 | XP_046798618.1 | 239 | NC_052532.1_cds_XP_046798618.1_11 | 720 | True | Gallus_gallus |
| LOC121106805 | XP_040503678.1 | 615 | NC_052532.1_cds_XP_040503678.1_12 | 1848 | True | Gallus_gallus |
| LOC121107380 | XP_040507277.1 | 615 | NC_052532.1_cds_XP_040507277.1_13 | 1848 | True | Gallus_gallus |
| LOC121107381 | XP_040507283.1 | 615 | NC_052532.1_cds_XP_040507283.1_14 | 1848 | True | Gallus_gallus |
| LOC121107383 | XP_040507286.1 | 615 | NC_052532.1_cds_XP_040507286.1_15 | 1848 | True | Gallus_gallus |
| ⋮ | | | | | | |

`identity` は protein と翻訳した cds が一致しているかどうかを表す。
