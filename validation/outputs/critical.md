# ResNet 논문의 실험 설계와 재현 가능성 검토

**판정:** 잔차 연결(residual connection)이 깊어진 네트워크의 최적화를 개선한다는 주장은, 파라미터 수를 맞춘 plain network 대조와 학습 오류 곡선으로 비교적 설득력 있게 뒷받침됩니다. 그러나 논문에 적힌 설정만으로 모든 수치를 그대로 재현하기는 어렵습니다. ImageNet 학습률 감소 규칙의 구체적 시점, 대부분 실험의 반복 실행 정보, 구현 환경이 빠져 있고, 검출 실험의 상세 구현을 설명한다는 appendix는 제공된 PDF에 없습니다. 이는 **제공된 자료의 한계**이며, 전체 출판물에 해당 정보가 없다는 뜻은 아닙니다. [인쇄 p. 774 (PDF p. 5), §4.1, Fig. 4·Table 2; p. 773 (PDF p. 4), §3.4; p. 777 (PDF p. 8), §4.3]

## 논문과 검토 범위

- Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun, *Deep Residual Learning for Image Recognition*, CVPR 2016. 제공 파일의 제목·저자·학회 메타데이터와 첫 페이지의 CVF Open Access 표시를 확인했습니다. DOI와 arXiv 버전 번호는 이 PDF에서 확인하지 못했으며 외부 조회는 하지 않았습니다.
- 원문: [resnet.pdf](../inputs.json). 계산 실험 중심의 논문으로, 지도 학습 이미지 분류와 객체 검출을 다룹니다.
- 본문 전체인 PDF pp. 1–8을 읽고, p. 9가 참고문헌임을 확인했습니다. 본문 pp. 1–8을 모두 렌더링해 주요 식·그림·표를 대조했습니다. 인쇄 페이지는 770–778이며 아래에는 인쇄 페이지와 PDF 파일 페이지를 함께 적었습니다.
- 별도 appendix, 코드, 체크포인트, 실행 로그, 실제 데이터는 제공되지 않았습니다. 아래의 “미보고”는 **이 PDF의 관련 본문에서 찾지 못했다**는 뜻이고, “자료로 확인 불가”는 필요한 부속 자료가 제공되지 않았다는 뜻입니다. 학습을 실행해 성능을 검증한 결과는 아닙니다.

## 무엇을 검증하려는 설계인가

저자들이 묻는 문제는 “층을 더 쌓으면 표현력이 늘어날 수 있는데, 왜 학습 오류부터 오히려 커지는가?”입니다. 목표 매핑을 직접 학습하는 대신 입력 $x$에 대한 변화 $F(x)$를 학습하고, $y=F(x,\{W_i\})+x$로 결합합니다. 입력과 출력 차원이 다르면 $W_sx$라는 projection을 사용할 수 있습니다. 원래 논문의 블록은 합산 **뒤에도 ReLU**를 적용합니다. 이 검토는 후속 pre-activation ResNet을 원래 모델과 혼동하지 않습니다. [p. 770 (PDF p. 1), §1; p. 771 (PDF p. 2), Fig. 2; p. 772 (PDF p. 3), §3.1–3.2, Eq. (1)–(2)]

가장 강한 대조 실험에서는 plain network에 shortcut만 추가하며, 차원이 증가할 때 zero padding을 쓰는 option A를 선택합니다. 따라서 plain/residual 쌍의 깊이·폭·파라미터 수가 같고, element-wise addition을 제외한 계산 구조도 같습니다. 이 설계는 단순히 파라미터를 늘려 좋아졌다는 설명을 상당 부분 배제합니다. [p. 772 (PDF p. 3), §3.2; p. 774 (PDF p. 5), §4.1, Table 2·Fig. 4]

| 실험 축 | 데이터와 평가 | 무엇을 비교하는가 | 설계상 주의점 |
|---|---|---|---|
| ImageNet 최적화 대조 | ILSVRC 2012, 1,000종; 학습 128만 장, validation 5만 장; Table 2는 10-crop top-1 오류(낮을수록 좋음) | 18/34-layer plain 및 같은 구조의 ResNet-A | Fig. 4의 validation 곡선은 center crop이므로 Table 2의 10-crop 수치와 동일한 측정값이 아님. [p. 773–774 (PDF pp. 4–5), §4.1·Table 2·Fig. 4] |
| ImageNet 확장·shortcut ablation | validation에서 top-1/top-5 오류 | A: 차원 증가 시 zero padding; B: 증가 시에만 projection; C: 모든 shortcut에 projection. 50/101/152-layer는 bottleneck과 B 사용 | B/C는 추가 파라미터가 있으므로 A/B/C의 차이를 shortcut 종류 하나의 효과로만 읽기 어려움. [p. 775 (PDF p. 6), Table 3·Fig. 5, §4.1] |
| CIFAR-10 깊이 분석 | 학습 5만 장, test 1만 장, 10종; 학습 일정은 45k/5k train/val로 정함; test는 원래 32×32 이미지의 single view | 20/32/44/56-layer plain/residual 대조 및 110/1202-layer residual 확장 | 110-layer에 초기 warm-up 예외가 있어 모든 깊이가 완전히 동일한 초기 일정은 아님. [p. 776 (PDF p. 7), §4.2·Table 6] |
| 객체 검출로의 전이 | VOC 2007/2012 test, COCO validation의 mAP(높을수록 좋음) | 같은 Faster R-CNN 구현에서 VGG-16을 ResNet-101로 교체했다고 저자들이 설명 | backbone 전체가 바뀌므로 잔차 연결만의 효과를 분리한 대조는 아님. 구현 세부는 미제공 appendix에 의존함. [p. 777 (PDF p. 8), §4.3·Tables 7–8] |

## 중심 주장과 성능 근거

| 주장 / 증거의 성격 | 직접 보고된 근거 | 평가와 해석 |
|---|---|---|
| 깊어진 plain net에서 degradation이 나타남 — 보고 결과 | ImageNet plain-18 top-1 27.94%, plain-34 28.54%. Fig. 4에서는 34-layer의 학습 오류도 더 높음. [p. 774 (PDF p. 5), Table 2·Fig. 4] | **분석자 해석:** 이 학습 조건에서 단순한 test 과적합만으로 설명하기 어렵다는 근거다. 모든 optimizer·학습 일정에서도 같은 문제가 불가피하다는 증명은 아니다. |
| 잔차 연결이 깊은 모델의 최적화를 개선함 — 보고 결과 | 같은 34-layer 대조에서 plain 28.54% → ResNet-A 25.03%, 즉 **3.51 percentage points** 낮은 validation top-1 오류. ResNet-A 18-layer 27.88% → 34-layer 25.03%. [p. 774 (PDF p. 5), Table 2·Fig. 4] | 차이는 표의 수치에서 계산했다. 학습 오류 곡선도 개선을 지지한다. 그러나 반복 실행의 분산이 없어 효과의 신뢰구간이나 작은 차이의 통계적 유의성은 알 수 없다. |
| 더 깊은 bottleneck ResNet에서 성능이 향상됨 — 보고 결과 | ImageNet validation, **10-crop**: ResNet-50/101/152의 top-1 오류 22.85/21.75/21.43%, top-5 오류 6.71/6.05/5.71%. [p. 775 (PDF p. 6), Table 3] | 깊이와 전체 용량·계산량이 함께 증가한다. Table 1의 계산량은 각각 3.8/7.6/11.3 billion FLOPs이며 논문은 multiply-adds라는 표현을 쓴다. 따라서 순수한 깊이 효과와 예산 증가 효과를 완전히 분리하지 않는다. [p. 772 (PDF p. 3), §3.3; p. 774 (PDF p. 5), Table 1] |
| 최고 성능 — 보고 결과 | ResNet-152 single model은 validation top-1 19.38%, top-5 4.49%; 다른 깊이의 6개 모델 앙상블은 test top-5 3.57%. [p. 775 (PDF p. 6), Tables 4–5; p. 776 (PDF p. 7), §4.1] | Table 4는 §3.4의 최선 결과용 fully-convolutional·다중 스케일 평가 문맥이며 Table 3의 10-crop과 구분해야 한다. 3.57%는 앙상블 및 test server 결과이므로 단일 모델 validation 수치와 직접 비교할 수 없다. [p. 773 (PDF p. 4), §3.4] |
| 1,000층 이상도 최적화할 수 있으나 일반화는 별개 — 보고 결과와 저자 해석 | CIFAR-10 ResNet-110: 5회 중 best 6.43%, mean±std **6.61±0.16%**; ResNet-1202: test 7.93%, 파라미터 19.4M. 1202-layer 학습 오류는 <0.1%라고 보고. [p. 776 (PDF p. 7), Table 6; p. 777 (PDF p. 8), Fig. 6·§4.2] | 저자들은 1202-layer가 더 나쁜 test 오류를 보인 이유로 과적합을 제시한다. 학습 가능성과 “계속 깊게 할수록 좋은 성능”은 구별해야 한다. |
| 다른 인식 과제에도 유용함 — 보고 결과 | COCO validation Faster R-CNN: VGG-16 → ResNet-101, mAP@.5 41.5 → 48.4%, mAP@[.5,.95] 21.2 → 27.2%. [p. 777 (PDF p. 8), Table 8] | 후자는 **6.0 percentage points**, 약 28% 상대 증가다. 저자들은 다른 검출 구현을 동일하게 유지했다고 주장하지만, 제공 자료로 세부 구현을 독립 확인할 수 없다. [동 페이지 §4.3] |

**그림에서 확인한 범위:** Fig. 4와 Fig. 6의 학습/validation 또는 test 곡선을 실제로 확인했으며, Fig. 7의 BN 이후·비선형성 이전 layer response의 표준편차가 residual network에서 대체로 작다는 패턴도 확인했습니다. Fig. 7은 잔차 변화가 작다는 해석과 정합적이지만, 그것만으로 성능 향상의 유일한 인과 기전이나 모든 층의 gradient 상태를 증명하지는 않습니다. [p. 774 (PDF p. 5), Fig. 4; p. 777 (PDF p. 8), Figs. 6–7·§4.2]

## 보고된 설정과 확인할 수 없는 설정

| 항목 | 상태 | 확인한 내용 / 남는 불확실성 |
|---|---|---|
| 데이터와 평가 split | **보고 / 부분 보고** | ImageNet 128만 train·5만 validation·10만 test, CIFAR-10 50k train·10k test와 schedule 결정용 45k/5k split을 명시. 그 5k의 정확한 샘플 ID·split seed와 데이터 라이선스 조건은 본문 미보고. [p. 773 (PDF p. 4), §4.1; p. 776 (PDF p. 7), §4.2] |
| ImageNet augmentation | **부분 보고** | 짧은 변을 [256,480]에서 무작위 선택, 224×224 random crop·horizontal flip, per-pixel mean subtraction. 색상 augmentation은 [21]의 방식이라고 참조하며 구체 수치·확률은 이 본문에 펼쳐 쓰지 않음. [p. 773 (PDF p. 4), §3.4] |
| CIFAR-10 augmentation | **보고 / 부분 보고** | per-pixel mean subtraction; 각 면 4-pixel padding, random 32×32 crop·horizontal flip; test는 single view. padding 값, 정확한 mean 산출 절차·값은 본문 미보고. [p. 776 (PDF p. 7), §4.2] |
| 구조 | **보고** | ImageNet의 stage별 채널·반복 횟수·downsampling은 Table 1, bottleneck은 Fig. 5. CIFAR는 $6n+2$층, stage별 {16,32,64} filters, 모든 shortcut option A. [p. 774 (PDF p. 5), Table 1; p. 775 (PDF p. 6), Fig. 5; p. 776 (PDF p. 7), §4.2] |
| 초기화·BN | **부분 보고** | 초기화는 [12] 참조, ImageNet은 scratch 학습. convolution 뒤 activation 앞 BN. BN epsilon·running statistics 설정과 초기화의 수식·구현은 이 본문만으로 완결되지 않음. [p. 773 (PDF p. 4), §3.4; p. 776 (PDF p. 7), §4.2] |
| 목적 함수·regularization | **부분 보고** | 분류기의 softmax와 weight decay $10^{-4}$, dropout 미사용은 명시. 구체적 loss 수식·reduction 규칙은 본문 미보고이므로 cross-entropy 구현을 선택한다면 재현자의 선택으로 기록해야 함. [p. 772 (PDF p. 3), §3.3; p. 773 (PDF p. 4), §3.4; p. 776 (PDF p. 7), §4.2] |
| ImageNet optimizer·schedule | **부분 보고** | SGD, batch 256, momentum 0.9, LR 0.1 시작, error plateau 때 10배 감소, 최대 $60\times10^4$ iterations. plateau의 판정 metric·window·threshold 및 모델별 실제 감소 시점·종료 iteration은 본문 미보고. [p. 773 (PDF p. 4), §3.4] |
| CIFAR optimizer·schedule | **보고 / 부분 보고** | batch 128, LR 0.1, 32k·48k iterations에서 10배 감소, 64k 종료. 110-layer는 LR 0.01로 train error <80%까지 warm-up(약 400 iterations). 1202-layer는 위 방식으로 학습했다고 쓰지만 깊이별 실행 로그는 없음. [p. 776 (PDF p. 7), §4.2; p. 777 (PDF p. 8), §4.2] |
| random seed·반복 실행 | **부분 보고** | ResNet-110은 5회 및 mean±std 보고. seed 값과 다른 ImageNet/CIFAR/검출 설정의 반복 수·분산은 본문 미보고. [p. 776 (PDF p. 7), Table 6; 관련 실험 §4.1–4.3] |
| 하드웨어·시간·메모리 | **부분 보고** | CIFAR는 2 GPUs로 학습. GPU 모델·training wall time·peak memory·ImageNet 하드웨어는 본문 미보고. FLOPs 및 일부 parameter counts는 Tables 1·6에 보고되어 있으나 실제 속도와 동일한 지표가 아님. [p. 774 (PDF p. 5), Table 1; p. 776 (PDF p. 7), Table 6·§4.2] |
| 분류 evaluation protocol | **부분 보고** | 10-crop, fully-convolutional + {224,256,384,480,640} 다중 스케일 score averaging, CIFAR single view는 명시. crop 좌표·score 결합의 구현 세부·평가 코드 버전은 본문 미보고. [p. 773 (PDF p. 4), §3.4; p. 776 (PDF p. 7), §4.2] |
| 검출 설정 | **자료로 확인 불가** | 본문은 Faster R-CNN·backbone·Table 7의 train/test 조합·Table 8의 validation 지표를 제공하지만, 상세 구현을 appendix로 넘김. 제공된 PDF에는 그 appendix가 없어 검출 training recipe와 competition 개선 전체를 검증할 수 없음. [p. 777 (PDF p. 8), §4.3·Tables 7–8] |
| 코드·체크포인트·dependencies | **본문 미보고 / 실물 확인 불가** | Caffe에서 구현할 수 있다는 설명은 있으나 이 PDF에 저자 release의 구체 URL·commit·checkpoint·library/CUDA 버전은 제시되지 않음. “당시/현재 코드가 없다”는 결론은 내리지 않음. [p. 771 (PDF p. 2), §1; 본문 전체 확인] |

## 실험의 강점과 한계

**강점 — 분석자 평가:** 가장 중요한 주장을 기존 SOTA와의 점수 비교만으로 설명하지 않고, 동일 구조의 plain/residual 대조로 검사합니다. 학습 오류와 평가 오류를 함께 보여 주고, ImageNet과 CIFAR-10에서 비슷한 현상을 확인하며, shortcut 종류와 깊이를 바꾼 실험을 제공합니다. 특히 1202-layer의 실패하는 일반화 결과도 보고해 “잔차 연결을 쓰면 깊이 증가가 언제나 이롭다”는 식의 과도한 결론을 피할 근거가 있습니다. [pp. 774–777 (PDF pp. 5–8), §4.1–4.2, Tables 2–6·Figs. 4·6]

**저자 스스로 남긴 문제:** plain network의 최적화 난점이 왜 발생하는지는 향후 연구로 남깁니다. 1202-layer의 test 성능 악화는 과적합 때문이라고 해석하고, 더 강한 regularization의 결합을 후속 과제로 제시합니다. bottleneck 선택도 허용 가능한 학습 시간이라는 실용적 제약에 따른 것이라고 설명합니다. [p. 774 (PDF p. 5), §4.1; p. 775 (PDF p. 6), §4.1; p. 777 (PDF p. 8), §4.2]

**분석자 비판:**

1. **불확실성 보고가 좁습니다.** 110-layer의 5회 결과는 유용하지만 34-layer option B/C의 작은 차이나 ImageNet depth 간 차이에는 반복 실행 분산이 없습니다. B/C의 작은 개선을 안정적인 우위로 단정할 수 없습니다. [p. 775 (PDF p. 6), Table 3; p. 776 (PDF p. 7), Table 6]
2. **깊이의 효과와 자원 효과를 나눠야 합니다.** 50→101→152층의 성능 향상은 계산량·용량도 늘린 결과입니다. 같은 학습/추론 budget에서 어떤 깊이가 최적인지 따로 검사하지 않습니다. [p. 774 (PDF p. 5), Table 1; p. 775 (PDF p. 6), Table 3]
3. **기전 설명은 실험적 정황입니다.** BN으로 신호와 gradient norm이 양호하다는 저자 설명과 layer-response 분석은 제공되지만, residual 재매개변수화가 optimizer의 수렴률을 개선하는 일반적 이론 증명이나 원인별 개입 실험은 없습니다. [p. 774 (PDF p. 5), §4.1; p. 777 (PDF p. 8), Fig. 7]
4. **적용 범위를 넘겨 읽으면 안 됩니다.** 평가가 표준 인식 benchmark에 집중되어 있으므로 distribution shift·corruption·adversarial robustness·실제 latency 우위는 이 논문으로 확립되지 않습니다. 검출 전이 역시 DenseNet 같은 다른 backbone에 대한 우위를 검사한 것은 아닙니다. [§4.1–4.3, pp. 773–777 (PDF pp. 4–8)]

재현의 첫 단계로는 **CIFAR-10 20/56-layer plain과 ResNet-A의 대조**가 적절합니다. 구조·일정·single-view 평가가 비교적 명확하고 shortcut 효과를 파라미터 증가와 분리할 수 있습니다. 먼저 모든 구현 선택과 seeds를 기록한 뒤 여러 seed에서 학습/테스트 오류를 함께 확인하고, 이후 110-layer의 warm-up과 5회 mean±std를 재현하는 순서가 좋습니다. ImageNet 최고 점수와 검출 결과의 정확한 재현은 학습률 로그·평가 코드·누락 appendix를 확보한 뒤 진행해야 합니다. 이는 논문을 바탕으로 제안한 **재현 계획**이지 실행한 결과가 아닙니다. [p. 776 (PDF p. 7), §4.2·Table 6; p. 773 (PDF p. 4), §3.4; p. 777 (PDF p. 8), §4.3]
