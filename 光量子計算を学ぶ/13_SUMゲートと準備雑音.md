# 13 SUMゲートと準備雑音

## 理想SUMの導出

制御C、標的Tに対して

$$
U_{\rm SUM}=e^{-i\hat q_C\hat p_T}
$$

を定義します。出力観測量は $U^\dagger \hat O U$。$A=i\hat q_C\hat p_T$ と置くと

$$
[A,q_T]=q_C,\qquad [A,p_C]=-p_T,
\qquad[A,q_C]=[A,p_T]=0.
$$

二重交換子はすべて消えるため

$$
q_C'=q_C,\quad p_C'=p_C-p_T,
\quad q_T'=q_T+q_C,\quad p_T'=p_T.
$$

qの格子番号を $c,t$ とすると $t\mapsto t+c$。2を法として見れば $t\mapsto t\oplus c$ なので、GKP符号空間ではCNOTになります。p側の逆符号は交換関係を保つために必要です。

## 有限スクイーズ補助モード

実装では補助モードA、Bのスクイーズされた直交位相振幅が残留雑音になります。論文のパラメータを

$$
g=\frac{1-R}{\sqrt R},\qquad
c=\sqrt{\frac{1-R}{1+R}},\qquad
d=\sqrt{\frac{R(1-R)}{1+R}}
$$

と略記し、$\eta_A=q_Ae^{-r_A}$、$\eta_B=p_Be^{-r_B}$ とすると

$$
\begin{aligned}
q_C'&=q_C-c\eta_A,\\
p_C'&=p_C-gp_T+d\eta_B,\\
q_T'&=q_T+gq_C+d\eta_A,\\
p_T'&=p_T+c\eta_B.
\end{aligned}
$$

$\operatorname{Var}(\eta_A)=v_A=e^{-2r_A}/2$、$\operatorname{Var}(\eta_B)=v_B=e^{-2r_B}/2$。単位ゲイン条件 $g=1$ を解くと、$u=\sqrt R$ に対して $u^2+u-1=0$ なので

$$
R=\left(\frac{\sqrt5-1}{2}\right)^2=\frac{3-\sqrt5}{2}\simeq0.381966.
$$

ここでRはこの回路のビームスプリッタパラメータです。$r_A,r_B\to\infty$ なら $\eta_A,\eta_B\to0$ で理想SUMに戻ります。

## 分散更新の行間

入力座標と補助雑音が相互に独立な場合、係数の二乗を掛けて足すと

$$
\begin{aligned}
v_{Cq}'&=v_{Cq}+c^2v_A,\\
v_{Cp}'&=v_{Cp}+g^2v_{Tp}+d^2v_B,\\
v_{Tq}'&=v_{Tq}+g^2v_{Cq}+d^2v_A,\\
v_{Tp}'&=v_{Tp}+c^2v_B.
\end{aligned}
$$

これがAppendix Aの準備雑音の分散式です。入力が相関していれば、たとえば $v_{Tq}'$ には $2g\operatorname{Cov}(q_T,q_C)$ が加わります。

さらに、同じ $\eta_A$ が二つの出力へ入るので、新しい雑音だけでも

$$
\operatorname{Cov}(q_C',q_T')\big|_{\rm added}=-cdv_A,
\qquad
\operatorname{Cov}(p_C',p_T')\big|_{\rm added}=cdv_B
$$

が生まれます。四つの分散だけでは回路の全雑音を表し切れません。独立入力の場合でも、理想SUM自体が $\operatorname{Cov}(q_C',q_T')$ に $gv_{Cq}$、$\operatorname{Cov}(p_C',p_T')$ に $-gv_{Tp}$ を生みます。

## 行列で一括する

$\boldsymbol x=(q_C,p_C,q_T,p_T)^T$ に対して

$$
S=\begin{pmatrix}1&0&0&0\\0&1&0&-g\\g&0&1&0\\0&0&0&1\end{pmatrix},
\quad
B=\begin{pmatrix}-c&0\\0&d\\d&0\\0&c\end{pmatrix}.
$$

したがって $\Sigma'=S\Sigma S^T+B\operatorname{diag}(v_A,v_B)B^T$。この形なら相関も失いません。これは本教材で補った共分散の整理であり、論文の未公開シミュレータ実装がこの行列をそのまま使ったという意味ではありません。

## 雑音を加える場所

このQND/SUMの有限補助スクイージング雑音は**準備段階**の $\mathcal N_{\rm prep}$ に含まれます。後で与えるMN-onの追加変位とは別です。MN-offでも準備雑音は残ります。

GKP格子補正を挟むと分布は条件付き・非Gaussianになり得るため、すべての回路を最後まで一つの分散だけで運ぶことも一般にはできません。各補正で測定記録、残留格子クラス、フレームを更新します。

確認：補助モードAの雑音が、制御qと標的qに逆符号で入ることから、追加共分散の符号を導いてください。

<!-- navigation -->

---

[[00_はじめに|学習目次]] · [[12_MBQCとQRL|前へ]] · [[14_資源とプロセッサのインターフェース|次へ]]
