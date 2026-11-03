# 記号と数式の対応表

案内：[[00_学習案内]]

## 同じ文字を使う異なる量

| 記号 | 意味 | 混同しない対象 |
|---|---|---|
| $q,p$ | 光の位相振幅 | 保持率 $q_L$、誤り確率 $p$ |
| $s_{\mathrm{GKP}}$ | 有効変位品質の dB 値 | シンドローム $\boldsymbol s_L$ |
| $r$ | スクイージングパラメーター | 候補リスク $r_L$、レール索引 $r_i$ |
| $z$ | 単一の GKP 剰余 | Pauli ラベル $(x,z)$ の第 2 ビット |
| $y_{\mathrm{prep}}$ | 工場の観測可能記録全体 | 新測定 $y_{\mathrm{post}}$、隠れた誤り |
| $a_L$ | 真のデータ Pauli クラス | 子資源のスロット番号 |
| $\hat a_L$ | 推定して補正するクラス | 既知の測定副作用フレーム |
| $e_L$ | 補正後の残留クラス | 採択事象 $A_L=1$ |
| $p_L(a\mid y)$ | 候補ごとのクラススコア | 集団の誤り率 $P_L$ |
| $\mathcal R_L$ | 候補の古典記録 | 名目消費量 $R_L^{\mathrm{GKP}}$ |
| $\mathcal S_L$ | 集団の性能記録 | シンプレクティック行列 $S_j$ |
| $\mathsf I_{\mathrm{LR}}$ | 接続仕様 | 恒等チャネル $\mathrm{id}$ |
| $\mathcal G$ | ゲージ群 | 評価グリッド $\mathcal G_{\mathrm{grid}}$ |
| $n(L)=4^L$ | 符号ブロックサイズ | 統計の採択試行数 $n$ |
| $D,G$ | データ、ゲージ | 12 子準備群の上付き $(D)$ |

Pauli クラスの教材内ビット規約は $I=(0,0)$、$X=(1,0)$、$Z=(0,1)$、$Y=(1,1)$ である。
整数ラベル 0〜3 を使う実装では、整数順を仮定せず、この対応表を確認して XOR する。

## 数式を探す

元の `main.tex` のラベル文字列を検索すると、対応式へ移動できる。
下表は導出のある章と、定義または模型として採用する式を分けている。

| 原稿ラベルまたは式 | 教材 | 扱い |
|---|---|---|
| `eq:gkp_digitized_error_main` | [[05_GKP符号と変位誤り#誤り率の積分を導く]] | 奇数の丸め区間から導出 |
| `eq:gkp_llr_main`、`eq:appA_gkp_llr` | [[06_GKP尤度とアナログ復号]] | 巻き込み和と正規化 |
| `eq:appA_gkp_zero_q`、`eq:appA_gkp_one_q` | [[05_GKP符号と変位誤り]] | 理想符号の定義 |
| `eq:appA_gkp_finite_energy_channel`、`eq:appA_gkp_random_displacement_channel` | [[05_GKP符号と変位誤り#理想格子と有限エネルギー]] | 有効雑音模型と限界 |
| `eq:appA_gkp_gaussian_noise_distribution`、`eq:appA_gkp_gaussian_shift_model` | [[04_光の連続変数とGaussian操作]]、[[05_GKP符号と変位誤り]] | 分布の定義 |
| `eq:appA_gkp_displacement_operator` | [[04_光の連続変数とGaussian操作#変位演算子]] | 共役変換 |
| $U_{\mathrm{SUM}}$、`eq:noisy_qnd_heisenberg` | [[04_光の連続変数とGaussian操作#SUM ゲートの導出]]、[[13_雑音モデルと共分散]] | 理想作用を導出、光学雑音式は採用 |
| `eq:noisy_qnd_variances` | [[13_雑音モデルと共分散#分散式の行間]] | 分散加算と相関 |
| `eq:c4_data_gauge_main` | [[07_C4符号とデータゲージ]] | 代数と明示的符号語 |
| `eq:label_preserving_H`、`eq:ds_swap_port_map`、`eq:ds_cnot_map` | [[08_C4の論理ゲートを導く]] | Pauli 共役変換による導出 |
| $n(L),d(L)$ | [[07_C4符号とデータゲージ#連接]] | 再帰的な符号計数 |
| `eq:c4_llr` | [[10_再帰工場とソフト復号]] | 事後確率の積と周辺化 |
| `eq:recursive_soft_resource_record`、`eq:recursive_soft_decoder_map` | [[10_再帰工場とソフト復号#候補ごとの記録]] | 記録と更新の定義 |
| `eq:frozen_decoder_class_scores`、`eq:supp_frozen_recursive_map` | [[10_再帰工場とソフト復号#厳密な符号処理と学習した推定]] | 固定推定器の構成 |
| `eq:policy_calibration_risk`、`eq:supp_decoder_uncertainty` | [[11_選別と独立評価#残留誤りを定義する]] | 決定規則 |
| `eq:policy_calibration_rank` | [[11_選別と独立評価#順位による二値選別]] | 保持数の計算 |
| `eq:soft_information_conditional_error`、`eq:hard_conditional_channel` | [[11_選別と独立評価#採択と失敗の確率]] | 条件付き確率 |
| `eq:policy_calibration_diagnostic` | [[11_選別と独立評価]] | 採択失敗数／採択数を選択データ上で計算 |
| `eq:known_frame_composition` | [[11_選別と独立評価#記録の更新を二重に数えない]] | ラベルの置換 |
| `eq:primary_residual_channel`、`eq:primary_canonical_failure` | [[03_Bell対とテレポーテーション]]、[[11_選別と独立評価]] | 残留分布とチャネルの条件 |
| `eq:logical_resource_interface`、`eq:logical_resource_performance_record` | [[12_工場プロセッサ境界]] | 仕様と性能記録の定義 |
| `eq:interface_cycle`、`eq:online_decoder_conditional_record` | [[12_工場プロセッサ境界#オンラインの合成]] | 条件付き写像の合成 |
| `eq:noise_scope_summary`、`eq:independent_mn_noise`、`eq:frozen_mn_on_variance` | [[13_雑音モデルと共分散#主評価の MN on]] | 宣言された物理模型 |
| `eq:qrl_t_epsilon`、`eq:qrl_noise_factors`、`eq:qrl_operation_variances` | [[13_雑音モデルと共分散#ゲート別 QRL の分散]] | 原稿のゲート別解析式を採用 |
| `eq:ordered_qrl_covariance` | [[13_雑音モデルと共分散#順序付き共分散伝播]] | 再帰代入で導出 |
| `eq:top_logical_use_convolution`、`eq:independent_postinjection_error` | [[13_雑音モデルと共分散#独立 Pauli 近似]] | XOR と独立性 |
| `eq:app_physical_flip` | [[05_GKP符号と変位誤り#誤り率の積分を導く]] | 尾部近似 |
| `eq:app_parity_flip` | [[13_雑音モデルと共分散#独立 Pauli 近似]] | 符号変数の期待値から導出 |
| `eq:recursive_l2_l5_ordering`、`eq:condition_specific_ordering_metric` | [[14_数値結果と統計的保証#12.25 dB の有限レベル改善]] | 観測結果と評価指標 |
| `eq:recursive_grid_transition_interval`、`eq:finite_level_ordering_criterion` | [[14_数値結果と統計的保証]] | グリッド基準の定義 |
| `eq:jeffreys_conventions`、`eq:cp_upper` | [[14_数値結果と統計的保証]] | Bayes 更新と二項分布の反転 |
| `eq:dataset_prep_recursive` | [[11_選別と独立評価]]、[[14_数値結果と統計的保証]] | レベル、品質、保持率、誤り率、区間、採択数、失敗数の集計レコード |
| `eq:nominal_resource_recursion`、`eq:resource_cliff_ratio` | [[15_資源数と時間の見積もり#名目消費量の漸化式]] | 規約と代入計算 |
| `eq:target_resource_policy_selection` | [[11_選別と独立評価#データの三つの役割]]、[[15_資源数と時間の見積もり]] | 選択集合内の最小費用候補を固定して独立確認 |
| `eq:source_cost_break_even` | [[15_資源数と時間の見積もり#品質の高い入力は無料ではない]] | 費用の不等式 |
| `eq:actual_retry_cost`、`eq:hard_recursive_delivery`、`eq:hard_recursive_resource` | [[15_資源数と時間の見積もり#実際の再試行費用]] | 再開過程と運用の区別 |
| `eq:swap_depth_benchmark`、`eq:bounded_online_depth`、`eq:pairing_width` | [[15_資源数と時間の見積もり#定深さと並列幅]] | 条件付き回路深さ |
| `eq:address_span`、`eq:operation_latency_decomposition`、$B_{\mathrm{delay}}$ | [[15_資源数と時間の見積もり#時間多重化の時間負担]] | 並列容量と切り上げ |
| `eq:source_limited_factory_rate`、`eq:stall_free_condition` | [[15_資源数と時間の見積もり#供給率]] | 単位時間の流量 |
| `eq:distance_depth_operating_points` | [[15_資源数と時間の見積もり]] | レベル 2 は $(d,N)=(4,16)$、レベル 3 は $(8,64)$ |

模型として与えられた値と、数学的に導ける恒等式を区別する。
たとえば追加 MN 分散の係数 $4\times10^{-0.2}$ は論文が指定した値であり、GKP 符号の定義から必然的に決まる定数ではない。
