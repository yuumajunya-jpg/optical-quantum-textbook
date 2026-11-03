# 光の連続変数と Gaussian 操作

前：[[03_Bell対とテレポーテーション]]　案内：[[00_学習案内]]　次：[[05_GKP符号と変位誤り]]

## 光のモードを振動子として扱う

**光学モード**：空間、時間、周波数などの波形を指定した、独立な電磁場の自由度である。
1 モードは量子調和振動子として表せる。
同じ光路を通っても、異なる時間波形のモードなら別の自由度になる。
論文ではこの区別を時空間アドレスで管理する。

消滅演算子 $a$ と生成演算子 $a^\dagger$ は $[a,a^\dagger]=1$ を満たす。
**直交位相振幅**を

$$
\hat q=\frac{a+a^\dagger}{\sqrt2},\qquad
\hat p=\frac{a-a^\dagger}{i\sqrt2}
$$

と定義すると $[\hat q,\hat p]=i$ になる。
論文はこの無次元規約を使う。
真空 $|0\rangle$ では $a|0\rangle=0$ なので

$$
\langle q^2\rangle=\frac12\langle aa^\dagger+a^\dagger a\rangle=\frac12,
\qquad \operatorname{Var}(p)=\frac12.
$$

光学真空の $|0\rangle$ と量子ビットの論理 $|0\rangle$ は異なる状態である。
GKP の論理 0 は真空ではない。

## スクイージング

**スクイージング**：一方の位相振幅の揺らぎを縮め、共役な位相振幅の揺らぎを広げる操作である。
理想的な $q$ スクイーズド真空では

$$
\operatorname{Var}(q)=\frac12e^{-2r},\qquad
\operatorname{Var}(p)=\frac12e^{2r}.
$$

積は $1/4$ で、不確定性関係 $\Delta q\Delta p\ge1/2$ と整合する。
両方の分散を同時にゼロにする操作ではない。
真空に対する分散の低下を dB で表すと

$$
s=-10\log_{10}\frac{\operatorname{Var}(q)}{1/2}
=\frac{20}{\ln10}r.
$$

これは実際のスクイーズド光に対する定義である。
[[05_GKP符号と変位誤り]] では同じ換算式を「有効な変位雑音の分散」に使うが、その物理的意味は区別する。

## Gaussian 状態と操作

**Gaussian 状態**：位相空間の Wigner 関数が Gaussian 関数になる状態である。
平均ベクトル $\mu$ と共分散行列 $\Sigma$ で定まる。
量子演算子の共分散は、$\Delta x_j=x_j-\langle x_j\rangle$ を使い、$\Sigma_{jk}=\langle\Delta x_j\Delta x_k+\Delta x_k\Delta x_j\rangle/2$ と対称化して定義する。
古典的なランダム変位だけを扱う場合は、通常の共分散に一致する。
**Gaussian 操作**は、位相振幅に線形な変換と変位を与え、Gaussian 状態を Gaussian 状態へ写す。
真空、スクイーズド光、ビームスプリッター、位相回転、ホモダイン測定はこの枠組みに入る。

位相振幅を $\boldsymbol x=(q_1,p_1,\ldots,q_n,p_n)^T$ に並べると、理想 Gaussian ユニタリは

$$
\boldsymbol x' = S\boldsymbol x+\boldsymbol d,\qquad S\Omega S^T=\Omega,
\quad \Omega=\bigoplus_j\begin{pmatrix}0&1\\-1&0\end{pmatrix}
$$

と表せる。
この条件を満たす $S$ を「シンプレクティック行列」と呼ぶ。
交換関係を保存する条件であり、単なる任意の実行列ではない。

## ホモダイン測定

**ホモダイン測定**：強い参照光との干渉を使って、選んだ角度の位相振幅を測る方法である。
教材では角度 $\theta$ に対して $q_\theta=q\cos\theta+p\sin\theta$ と定義する。
$\theta=0$ なら $q$、$\theta=\pi/2$ なら $p$ を測る。
文献によって角度の原点や符号が違うため、QRL の図に出る測定基底と合わせる必要がある。

同じモードの未知の $q,p$ を同時に無雑音で得ることはできない。
シミュレーターが持つ変位座標の全部を、実験で読み出せる特徴量として扱ってはいけない。
論文の復号器は、許された測定結果と既知の記録だけを入力とする。

## 変位演算子

論文は変位を

$$
D(\xi_q,\xi_p)=e^{-i\xi_q\hat p}e^{i\xi_p\hat q}
$$

と定義する。
交換子展開を使えば

$$
D^\dagger qD=q+\xi_q,\qquad D^\dagger pD=p+\xi_p
$$

を得る。
2 つの指数の順序を逆にすると位相が付くが、$D\rho D^\dagger$ の大域位相は消える。
この変位をランダムに加えるモデルが論文の雑音モデルである。

## SUM ゲートの導出

**SUM ゲート**：制御モードの $q$ を標的モードの $q$ に加える 2 モード Gaussian ゲートである。
論文の規約では

$$
U=\exp(-i q_Cp_T).
$$

$U^\dagger q_T U$ を計算する。
$[i q_Cp_T,q_T]=q_C$、$[i q_Cp_T,q_C]=0$ なので、高次項は消える。
同様に $[i q_Cp_T,p_C]=-p_T$ から

$$
q_C'=q_C,\quad p_C'=p_C-p_T,\quad
q_T'=q_T+q_C,\quad p_T'=p_T.
$$

$q$ に加算するだけでなく、$p$ に逆向きの作用が必要なのは、交換関係を保存するためである。
たとえば $[q_T+q_C,p_C-p_T]=i-i=0$ となり、出力の別モード同士は可換のままである。

GKP の格子点で $q_C=(2m+a)\sqrt\pi$、$q_T=(2n+b)\sqrt\pi$ とすると

$$
q_T'=[2(m+n)+a+b]\sqrt\pi.
$$

標的の格子の偶奇は $a\oplus b$ になるので、SUM は GKP 上の CNOT を実現する。
有限スクイージングを使う実装の雑音は [[13_雑音モデルと共分散]] で導く。

論文との対応：付録 A、`eq:appA_gkp_displacement_operator`、`eq:noisy_qnd_heisenberg`。

次：[[05_GKP符号と変位誤り]]
