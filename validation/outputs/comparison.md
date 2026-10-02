# ResNet과 DenseNet: 방법, 성능 근거, 사용할 조건

**핵심 결론:** ResNet은 잔차 합산으로 깊은 네트워크의 최적화 문제를 다루며, DenseNet은 앞선 특징을 채널 방향으로 이어 붙여 재사용하는 구조로 정확도 대비 파라미터·계산량을 줄이려 합니다. 제공된 두 논문에서 가장 강한 ResNet 근거는 동일 구조 plain/residual 대조이고, DenseNet의 비교 강점은 논문 내부의 공통 ImageNet 평가 환경에서 나타난 효율성입니다. **실제 inference latency, peak memory, 새로운 도메인에서의 성능까지 어느 쪽이 우세한지는 이 자료만으로 결정할 수 없습니다.** [R p. 774 (PDF p. 5), Table 2·Fig. 4; D pp. 4705–4706 (PDF pp. 6–7), §4.4·Fig. 3]

## 자료와 비교 범위

| 약칭 | 제공된 정확한 문헌 | 원문과 범위 |
|---|---|---|
| R | Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun, *Deep Residual Learning for Image Recognition*, CVPR 2016 | [resnet.pdf](../inputs.json), 인쇄 pp. 770–778 = PDF pp. 1–9. 본문 pp. 1–8을 읽고 시각 검토, p. 9 참고문헌 확인. 검출 상세를 설명한다는 appendix는 제공되지 않음. |
| D | Gao Huang, Zhuang Liu, Laurens van der Maaten, Kilian Q. Weinberger, *Densely Connected Convolutional Networks*, CVPR 2017 | [densenet.pdf](../inputs.json), 인쇄 pp. 4700–4708 = PDF pp. 1–9. 본문 pp. 1–8을 읽고 pp. 1,3–8의 중심 그림·표·식을 시각 검토, p. 9의 ResNet 관련 참고문헌 확인. |

둘 다 제공된 CVF Open Access PDF와 학회 메타데이터를 기준으로 식별했습니다. DOI·arXiv revision은 이 파일에서 확인되지 않았습니다. 외부 저장소·코드·후속 benchmark를 조회하지 않았으며, 여기서의 사용 조건은 **이 두 논문의 증거에 근거한 분석자 판단**입니다. 아래의 미보고는 해당 제공 PDF 범위에 한정합니다.

## 연결 방식의 차이가 만드는 동작

**ResNet:** 입력 특징 $x$를 shortcut으로 전달하고 학습된 변화 $F(x)$와 원소별로 더합니다. 핵심 식은 $y=F(x,\{W_i\})+x$이며, 차원이 바뀔 때 projection $W_sx$ 또는 zero padding을 사용합니다. 원래 R 논문은 합산 후 ReLU를 적용합니다. ImageNet의 깊은 모델은 1×1→3×3→1×1 bottleneck을 사용합니다. 입력 표현을 계속 수정하는 방식이라고 이해하면 됩니다. [R p. 771 (PDF p. 2), Fig. 2; p. 772 (PDF p. 3), Eq. (1)–(2); p. 775 (PDF p. 6), Fig. 5]

**DenseNet:** 같은 dense block 안에서 앞선 모든 층의 특징을 그대로 모아 다음 층의 입력으로 씁니다. $x_\ell=H_\ell([x_0,x_1,\ldots,x_{\ell-1}])$에서 대괄호는 channel concatenation입니다. 각 층은 성장률(growth rate) $k$개의 새 feature maps를 추가합니다. 기본 $H_\ell$은 BN→ReLU→3×3 convolution이고, 공간 크기가 달라지는 지점은 transition layer로 처리하므로 **전체 네트워크의 모든 층을 크기와 무관하게 직접 concat한다는 뜻은 아닙니다.** [D p. 4702 (PDF p. 3), §3, Eq. (2)·Fig. 2; p. 4700 (PDF p. 1), Fig. 1]

DenseNet-B는 3×3 앞의 1×1 bottleneck이 4k개 feature maps를 만들도록 하고, DenseNet-C는 transition 출력 채널을 $\lfloor\theta m\rfloor$로 줄입니다. 실험의 compression factor는 θ=0.5이며 둘을 함께 쓰면 DenseNet-BC입니다. ImageNet 실험은 모두 이 BC 구조를 사용합니다. 따라서 효율성 결과를 “concat 연산 하나의 효과”로만 귀속할 수는 없습니다. 구조·정규화 순서·bottleneck·compression까지 함께 고려해야 합니다. [D p. 4703 (PDF p. 4), §3·Table 1]

이 계보는 단순한 발표 연도 추측이 아닙니다. D는 R을 직접 인용하며, residual network의 특징 중복과 stochastic depth 관찰에서 일부 영감을 받았다고 설명합니다. D의 **pre-activation ResNet** 비교는 별도 논문 *Identity Mappings in Deep Residual Networks* [12]에 해당하며, 이 요청의 R 원문 [11]과 구분해야 합니다. [D p. 4701 (PDF p. 2), §1–2; p. 4708 (PDF p. 9), References [11]–[13]]

## 실험 조건을 정규화한 비교

| 항목 | R: 원래 ResNet 논문 | D: DenseNet 논문 | 비교에 주는 의미 |
|---|---|---|---|
| 연구 초점 | 층 증가 때 학습 오류가 악화하는 degradation, 잔차 학습으로 최적화 개선. [R pp. 770–772 (PDF pp. 1–3), §§1·3.1] | 앞선 특징의 직접 접근·재사용과 정확도 대비 model compactness. [D pp. 4700–4703 (PDF pp. 1–4), §§1·3] | 두 논문이 강조하는 성능 문제와 가장 설득력 있는 실험이 다름. |
| 과제·데이터 | 지도 분류: ImageNet 2012·CIFAR-10; 전이: VOC·COCO 검출. [R pp. 773·776–777 (PDF pp. 4·7–8), §4] | 지도 분류: CIFAR-10·CIFAR-100·SVHN·ImageNet 2012. [D pp. 4703–4704 (PDF pp. 4–5), §4.1] | 공통 비교 과제는 CIFAR-10과 ImageNet 분류. D의 검출 성능은 이 논문에서 평가되지 않음. |
| 분류 출력·목적 | global average pooling·softmax classifier. 손실의 정확한 수식은 본문 미보고. [R p. 772 (PDF p. 3), §3.3; p. 776 (PDF p. 7), §4.2] | global average pooling·softmax classifier. 손실의 정확한 수식은 본문 미보고. [D p. 4703 (PDF p. 4), §3·Table 1] | 공통된 지도 분류 설정이나, 제공 자료만으로 loss 구현까지 동일하다고 확인할 수 없음. |
| CIFAR 전처리·augmentation | per-pixel mean subtraction; 4-pixel padding·32×32 random crop·flip. [R p. 776 (PDF p. 7), §4.2] | channel mean/std normalization; mirroring/shifting, “+” 표시. 최종 CIFAR run은 50k train 전체 사용. augmentation 없는 데이터에는 dropout 0.2. [D p. 4704 (PDF p. 5), §4.1–4.2·Table 2] | C10와 C10+를 섞으면 안 되며, R/D의 학습 pipeline도 완전히 같지 않음. |
| CIFAR 학습 예산 | batch 128, 64k iterations; LR 감소 32k·48k; 110-layer warm-up. [R p. 776 (PDF p. 7), §4.2] | batch 64, 300 epochs; LR 감소 150·225 epochs. [D p. 4704 (PDF p. 5), §4.2] | 원문 간 CIFAR 수치의 차이를 architecture의 순수 인과 효과로 볼 수 없음. |
| optimizer·regularization | SGD, momentum 0.9, weight decay $10^{-4}$, dropout 없음. [R p. 773 (PDF p. 4), §3.4; p. 776 (PDF p. 7), §4.2] | SGD, Nesterov momentum 0.9, no dampening, weight decay $10^{-4}$; augmentation 없는 C10/C100/SVHN에서 dropout 0.2. [D p. 4704 (PDF p. 5), §4.2] | dropout 및 momentum 구현 차이를 점수 해석에 반영해야 함. |
| ImageNet 학습 | batch 256, LR 0.1, plateau에서 10배 감소, 최대 600k iterations. random resize/crop·flip·color augmentation. [R p. 773 (PDF p. 4), §3.4] | ResNet의 공개 Torch 구현을 채택하고 preprocessing·optimization을 공통으로 유지했다고 설명. 기본 batch 256·90 epochs·LR 감소 30·60 epochs. [D pp. 4704–4706 (PDF pp. 5–7), §4.2·4.4] | D의 내부 비교가 R의 원래 recipe보다 더 직접적이다. 단, 제공 자료로 코드 자체의 동일성은 감사하지 않았음. |
| ImageNet 최대 모델 예외 | 152-layer bottleneck, Table 1에 구조·계산량. [R p. 774 (PDF p. 5), Table 1] | DenseNet-161은 memory constraint 때문에 batch 128·100 epochs, 90 epoch에 세 번째 LR 감소. [D pp. 4704·4706 (PDF pp. 5·7), §4.2·4.4] | DenseNet-161을 완전히 동일한 학습 budget의 대조로 취급하면 안 됨. |
| 평가·반복 | ImageNet 10-crop 및 최선 결과용 multi-scale; CIFAR single view. ResNet-110만 5회 mean±std 명시. [R pp. 773·775–776 (PDF pp. 4·6–7), §3.4·Tables 3–6] | ImageNet single/10-crop 각각 보고; 각 task·model setting의 test error는 한 번만 평가했다고 명시. [D p. 4704 (PDF p. 5), §4.1–4.2; p. 4705 (PDF p. 6), Table 3] | 점수가 작게 차이 날 때 안정적인 순위인지 판단할 반복 분산이 부족함. |
| 자원·재현 자료 | 일부 FLOPs·parameter count; CIFAR 2 GPUs. 제공 PDF에 release URL·환경 버전 미보고; 검출 appendix 미제공. [R pp. 774·776–777 (PDF pp. 5·7–8), Tables 1·6·§4.2–4.3] | 코드·pretrained models URL을 명시하지만 실제 파일·환경·commit은 미확인. implementation memory inefficiency로 >30M 모델 실험이 제한됐다고 저자들이 설명. [D p. 4700 (PDF p. 1), Abstract; p. 4706 (PDF p. 7), footnote 2] | 작은 weight 파일이 낮은 activation memory·짧은 latency를 보장하지 않음. 두 모델의 같은 hardware 실측이 필요함. |

## 성능 근거: 공통 조건과 문맥 수치를 나누어 읽기

### 공통 평가 조건에서 볼 수 있는 효율성 근거

D의 ImageNet Fig. 3은 **single-crop validation top-1 오류**를 파라미터 수와 test-time FLOPs에 대해 그립니다. preprocessing·optimization을 공통으로 유지했다는 §4.4 설명과 연결되므로, 두 원문에서 각자의 최고값을 끌어와 비교하는 것보다 타당한 증거입니다. 다만 모델 규모가 정확히 같은 쌍을 모두 제공하는 것은 아니므로, 동일 규모의 엄격한 순위보다 **정확도 대 자원 효율 곡선**으로 해석해야 합니다. [D pp. 4705–4706 (PDF pp. 6–7), Fig. 3·§4.4]

| 비교 | 논문이 제공하는 근거 | 해석의 한계 |
|---|---|---|
| DenseNet-201 vs ResNet-101 | D 본문은 약 20M parameters의 DenseNet-201이 40M 초과의 ResNet-101과 비슷한 single-crop validation 오류를 얻었다고 설명. Fig. 3의 점들과 부합함. DenseNet-201의 정확한 표 값은 top-1 **22.58%**, top-5 **6.34%**. [D p. 4705 (PDF p. 6), Table 3·Fig. 3; p. 4706 (PDF p. 7), §4.4] | ResNet-101의 이 실험에 대한 정확한 오류는 D의 해당 표에 없어 그래프에서 임의로 소수점을 읽지 않음. “더 적은 파라미터로 비슷한 오류”라는 효율성 근거이며, 동일 파라미터 수의 통제 대조는 아님. |
| 계산량을 맞춘 영역 | D는 ResNet-50 정도의 계산량을 쓰는 DenseNet이 ResNet-101 정도의 정확도를 보였다고 설명하며 Fig. 3 우측에 근거를 제시. [D p. 4706 (PDF p. 7), §4.4; p. 4705 (PDF p. 6), Fig. 3] | 이 논문 내부의 계산량 비교로 한정. FLOPs를 실제 latency로 바꾸거나, 서로 다른 논문의 operation counting을 무조건 같다고 가정하지 않음. R의 원문은 FLOPs에 “multiply-adds”라는 설명을 씀. [R p. 772 (PDF p. 3), §3.3] |

### 같은 benchmark이지만 recipe·모델 규모가 다른 문맥 근거

아래 표는 보고값을 보존하기 위한 표입니다. **모든 행을 한 leaderboard로 정렬하거나 수치 차이를 concat 대 addition의 효과라고 해석하지 않습니다.**

| 논문·모델 | 데이터·split·평가 | 보고 오류(%, 낮을수록 좋음) | 자원 / 중요한 조건 |
|---|---|---|---|
| R ResNet-50 | ImageNet validation, 10-crop | top-1 **22.85**, top-5 **6.71** | Table 1 계산량 3.8 billion FLOPs. [R p. 775 (PDF p. 6), Table 3; p. 774 (PDF p. 5), Table 1] |
| R ResNet-101 | 같은 R 10-crop | **21.75 / 6.05** | 7.6 billion FLOPs. [R p. 774 (PDF p. 5), Table 1; p. 775 (PDF p. 6), Table 3] |
| R ResNet-152 | 같은 R 10-crop | **21.43 / 5.71** | 11.3 billion FLOPs. [R p. 774 (PDF p. 5), Table 1; p. 775 (PDF p. 6), Table 3] |
| D DenseNet-121, k=32 | ImageNet validation, 10-crop | **23.61 / 6.66** | 다른 학습 recipe·모델 규모. Table 3 괄호 안이 10-crop 값. [D p. 4705 (PDF p. 6), Table 3; p. 4704 (PDF p. 5), §4.2] |
| D DenseNet-169, k=32 | 같은 D 10-crop | **22.08 / 5.92** | 같은 D 기본 schedule. [D p. 4705 (PDF p. 6), Table 3] |
| D DenseNet-201, k=32 | 같은 D 10-crop | **21.46 / 5.54** | 20M parameters라는 본문 설명. [D p. 4705 (PDF p. 6), Table 3; p. 4706 (PDF p. 7), §4.4] |
| D DenseNet-161, k=48 | 같은 D 10-crop | **20.85 / 5.30** | batch 128·100 epochs의 예외. [D p. 4705 (PDF p. 6), Table 3; pp. 4704·4706 (PDF pp. 5·7), §4.2·4.4] |
| R ResNet-110 | CIFAR-10 test, augmentation, single view | best **6.43**, 5회 mean±std **6.61±0.16** | 1.7M parameters. best와 mean을 섞지 않음. [R p. 776 (PDF p. 7), Table 6] |
| D DenseNet-BC-100, k=12 | C10+ test | **4.51** | 0.8M parameters, D의 batch 64·300 epochs. D Table 2에 인용된 원래 ResNet-110 값은 **6.61**이다. [D p. 4704 (PDF p. 5), Table 2·§4.2] |
| D가 비교한 pre-activation ResNet-1001 | C10+ test | **4.62** | 10.2M parameters; **R 논문의 ResNet-1202와 다른 모델**. [D p. 4704 (PDF p. 5), Table 2] |
| D DenseNet-BC-190, k=40 | C10+ / C100+ test | **3.46 / 17.18** | 25.6M parameters. 매우 작은 DenseNet의 결과가 아님. [D p. 4704 (PDF p. 5), Table 2] |

R의 유명한 **3.57%**는 6개 모델 앙상블의 ImageNet **test top-5** 오류입니다. 이를 D의 single model validation top-1 또는 10-crop top-5와 비교해 승자를 정하면 안 됩니다. R의 single model 최선값인 top-5 **4.49%**도 multi-scale 평가 문맥에 있으므로 위 10-crop 표와 구분해야 합니다. [R p. 773 (PDF p. 4), §3.4; p. 775 (PDF p. 6), Tables 4–5; p. 776 (PDF p. 7), §4.1]

## 왜 개선됐다는 설명을 어디까지 믿을 수 있는가

**ResNet의 author claim:** identity에 가까운 변화를 학습하도록 재매개변수화하면 더 쉽게 최적화할 수 있다는 가설입니다. 동일 구조 plain/residual의 training error 차이는 강한 경험적 근거이고, Fig. 7의 작은 residual responses는 이 동기와 정합적입니다. 하지만 모든 optimizer에서의 수렴 보장이나 순수한 vanishing-gradient 해결 증명은 아닙니다. R 자체도 BN을 사용한 plain net에서는 gradient가 소실되지 않았다고 설명합니다. [R pp. 772·774·777 (PDF pp. 3·5·8), §3.1·4.1·4.2, Figs. 4·7]

**DenseNet의 author claim:** 짧은 연결이 정보·gradient 전달을 개선하고 feature reuse를 유도해 파라미터를 줄인다는 설명입니다. Fig. 4는 BC variant의 효율성을, Fig. 5는 C10+의 40-layer, k=12 모델에서 이전 층의 특징을 입력으로 받는 연결 가중치를 보여 줍니다. 실제 heatmap에서도 여러 앞선 층에 weight가 분산된 것을 확인했습니다. 다만 평균 절대 weight는 feature 의존도의 **surrogate**이므로, 연결을 제거했을 때의 성능이나 인과적 중요도를 직접 측정한 것은 아닙니다. [D p. 4706 (PDF p. 7), Fig. 4·§5; p. 4707 (PDF p. 8), Fig. 5·“Feature Reuse”]

**공통 한계 — 분석자 평가:** 일부 결과 차이는 학습 schedule·normalization·regularization·용량 차이와 함께 나타납니다. R은 1202-layer 과적합을 인정하며, D도 SVHN에서 더 깊은 BC 모델의 개선이 없고 augmentation 없는 C10에서 k 증가로 5.77→5.83% 악화한 경우를 설명합니다. 따라서 어느 구조도 “깊거나 크면 항상 좋다”거나 “과적합이 사라진다”는 결론을 지지하지 않습니다. [R p. 777 (PDF p. 8), §4.2; D p. 4705 (PDF p. 6), §4.3]

## 어떤 조건에서 사용할 것인가

| 필요한 조건 | 이 자료에 근거한 선택 | 선택 전에 확인할 것 |
|---|---|---|
| 깊이 증가가 학습 오류까지 악화하는 문제를 분석하거나, residual 효과를 통제 대조로 배우고 싶음 | **원래 ResNet부터**. R의 parameter-matched plain/residual 설계가 직접 답을 제공함. [R p. 774 (PDF p. 5), Table 2·Fig. 4] | 후속 pre-activation 모델과 원래 post-addition ReLU 모델을 구분하고, 같은 schedule·seed 세트로 비교. |
| 이미지 분류에서 저장할 파라미터 수나 산술 계산 예산이 우선이고, 중간 특징을 보존·재사용하고 싶음 | **DenseNet-BC를 우선 후보로**. D의 공통 ImageNet 효율 곡선과 small-model CIFAR 분석이 근거임. [D pp. 4705–4706 (PDF pp. 6–7), Figs. 3–4] | 실제 target framework에서 peak memory·latency를 측정. 저자 구현에도 memory inefficiency가 보고되어 weight 수만으로 자원을 판단할 수 없음. [D p. 4706 (PDF p. 7), footnote 2] |
| VOC/COCO 검출로 전이할 때 두 논문 중 직접적인 실험 근거가 필요함 | **ResNet-101이 근거가 더 직접적**. R은 Faster R-CNN backbone 교체의 mAP를 보고, D는 feature transfer를 향후 연구로 남김. [R p. 777 (PDF p. 8), Tables 7–8·§4.3; D p. 4707 (PDF p. 8), §6] | 미제공 R appendix·검출 recipe를 확보. 이 선택은 D보다 검출 정확도가 높다는 비교 결과가 아님. |
| SVHN·CIFAR-100과 유사한 과제에서 출발할 본문 실험이 필요함 | **DenseNet 논문에 더 직접적인 데이터별 근거가 있음**. D Table 2는 이들 과제를 평가하며 R의 분류 실험은 CIFAR-10·ImageNet임. [D p. 4704 (PDF p. 5), Table 2; R pp. 773·776 (PDF pp. 4·7), §§4.1–4.2] | 데이터 크기·augmentation 조건을 맞추고 더 깊은 모델이 반드시 개선되지 않는 SVHN 결과도 고려. [D p. 4705 (PDF p. 6), §4.3] |
| mobile latency·training activation memory·distribution shift robustness가 결정적임 | **두 논문으로 승자 결정 보류**. 동일 target hardware의 latency·memory와 해당 shift 평가가 보고되지 않음. [R pp. 773–777 (PDF pp. 4–8), §4; D pp. 4703–4706 (PDF pp. 4–7), §4·footnote 2] | 같은 입력 크기·batch·precision·budget·평가 split으로 두 후보를 직접 실측. 이는 추가 평가 제안이지 확인된 결과가 아님. |

논문을 읽는 순서는 R의 **Fig. 2 → §3.2 → Table 2·Fig. 4**에서 최적화 대조를 이해한 뒤, D의 **Eq. (2) → §3의 B/C 설계 → Table 2의 footnote → §4.4·Fig. 3 → Fig. 5**로 이어가는 편이 효율적입니다. 남는 핵심 질문은 “같은 파라미터·학습·실제 지연시간 budget에서 효율성 우위가 유지되는가”, “feature reuse의 이득이 연결 제거 실험에서도 나타나는가”, “검출이나 데이터 이동에서도 어떤 구조가 더 나은가”입니다. 이들은 제공된 두 논문만으로 닫히지 않은 질문입니다.
