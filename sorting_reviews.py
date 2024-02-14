############################################
# SORTING REVIEWS
############################################

import pandas as pd
import math
import scipy.stats as st

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

###################################################
# Up-Down Diff Score = (up ratings) − (down ratings)
###################################################

#Kullanılacak olan yöntem Up-Down Diff Score yöntemidir. Up-rate'ler ile down rate'leer arasındaki farkı alacağız ve bir sıralama yapacağz


# Review 1: 600 up 400 down total 1000
# Review 2: 5500 up 4500 down total 10000



def score_up_down_diff(up, down):
    return up - down

# Review 1 Score:
score_up_down_diff(600, 400)

# Review 2 Score
score_up_down_diff(5500, 4500)

#review 'in score 200 iken review 2''nin score 1000 çıkıyor halbuki yüzdelik bazda inclendiinde review 1'in daha yüksek olduğu görülüyor
#o zaman bu yöntemi kullanmak mantıklı değildir

#birçok e-ticaret firmasında yorum sıralamasında bu yanlış skorlama yönteminin kullanıldığı malesef görülecektir

###################################################
# Score = Average rating = (up ratings) / (all ratings)
###################################################
#up oranı yöntemi değerlendirmesi


def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up + down)

score_average_rating(600, 400)   #0.6
score_average_rating(5500, 4500)  #0.55
#diğer yönteme göre bu yöntem daha başarılı sonuç elde etmiştir


# Review 1: 2 up 0 down total 2
# Review 2: 100 up 1 down total 101

score_average_rating(2, 0)    #1
score_average_rating(100, 1)  #0.99

#sıralama yapıldığında review 1 yukarıda olacaktır
#normalde kazanması gereken  bu değildir, bu yöntem frekans yüksekliğini göz önünde bulunduramadı

#peki biz neden önce olmayacakları değerlendiriyoruz?
#literatüre bakıldığında wilson_lower_bound yöntemi'de bu bakış açısını tercih etmiştir
#ele alınan örnekleri ve yerli bazı siteler incelendiğinde doğru olamayacak yaklaşımların ya da bu yaklaşımların bile olmadığı görülecektir
#dolayısıyla yanlışı biliyor olmak gerekliliğiyle birlikte doğru yöntemi geliştirmemize yardımcı olacaktır

#öyle bir yöntem bulunmalı ki hem frekans hem oran bilgisini elinde tutarak değerlendirme yapsın

###################################################
# Wilson Lower Bound Score
###################################################

#Yöntem açıklaması : herhangi ikili interaction'lar barındıran item, product ya da review'ı skorlama imkanı sağlar
#youtube'daki beğeniler like/dislike, soru cevap formlarındaki yorumlar helpful/not helpfull şeklindedir
#ikili etkileşimler sonucu ortaya çıkan bütün ölçme problemlerinde yardımı dokunur

#Bernoulli bir olasılık dağılımıdır ve ikili olayların olasılığını hesaplamak için kullanılır
#örneğin bir yazı tura olayının yazı gelmesi durumunu, iki sonucu olan bir olayın nasıl gerçekleşebileceeği olasılığını hesaplamak için kullanılır

#bizim elimizde müşterilerle ilgili bütün etkileşimler yok, yani diyelimki bir kulllanıcı bir yorum yaptı ve buna bazı etkileşimler geldi, beğendi beğenmedi gibi ama tamamanı bilmiyoruz, bütün veri elimde yok fakat elimde bir örneklem vardır, örneğin 600 like 400 dislike gibi
#buradan bir genelleme yapmak istiyoruz, bu değeri bütün kitleye yansıtabilelim diye dolayısıyla bu problemi bir olasılık problemi olarak ele aldığımızda ve bu değerlerden bir güven aralığı hesapladığımızda  elimizde çok değerli bir bilgi olacaktır


# 600-400
# 0.6     --> up oranı
# 0.5 0.7
# 0.5

#up oranı için bir güven aralığı hesaplandığında şunu diyor oluruz; 100 kullanıcan 95'i yorumla ilgilli bir etkileşim sağladığında %5 yanılma payım olmakla birlikte bu yorumun up oranı %5 ile %7 arasında olacaktır denir



def wilson_lower_bound(up, down, confidence=0.95):
    """
    Wilson Lower Bound Score hesapla

    - Bernoulli parametresi p için hesaplanacak güven aralığının alt sınırı WLB skoru olarak kabul edilir.
    - Hesaplanacak skor ürün sıralaması için kullanılır.
    - Not:
    Eğer skorlar 1-5 arasıdaysa 1-3 negatif, 4-5 pozitif olarak işaretlenir ve bernoulli'ye uygun hale getirilebilir.
    Bu beraberinde bazı problemleri de getirir. Bu problemlerden dolayı; bayesian average rating yapmak gerekir.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


wilson_lower_bound(600, 400)     #0.5693094295142663
wilson_lower_bound(5500, 4500)   #0.5402319557715324

wilson_lower_bound(2, 0)      #0.3423802275066531
wilson_lower_bound(100, 1)    #0.9460328420055449


###################################################
# Case Study
###################################################

# ödev bilinen e-ticaret firmalarına git ve öğrenilen bilgileri dene
# bu veri seti bir e-ticaret firmasından alınma ve kulanıcının yorumunun faydalı bulunma ya da bulunmama adedini içermektedir


up = [15, 70, 14, 4, 2, 5, 8, 37, 21, 52, 28, 147, 61, 30, 23, 40, 37, 61, 54, 18, 12, 68]
down = [0, 2, 2, 2, 15, 2, 6, 5, 23, 8, 12, 2, 1, 1, 5, 1, 2, 6, 2, 0, 2, 2]
comments = pd.DataFrame({"up": up, "down": down})



# score_pos_neg_diff
comments["score_pos_neg_diff"] = comments.apply(lambda x: score_up_down_diff(x["up"],
                                                                             x["down"]), axis=1)

# score_average_rating
comments["score_average_rating"] = comments.apply(lambda x: score_average_rating(x["up"], x["down"]), axis=1)

# wilson_lower_bound
comments["wilson_lower_bound"] = comments.apply(lambda x: wilson_lower_bound(x["up"], x["down"]), axis=1)



#bu sıralama sitede yer alan sıralamadır ve 5.,7., 11. satırlardan sıralamada bir problem olduğu anlaşılmaktadır
#pazar yeri için negatif yorum barındırıyor olması, baskılanması ve gerilere atılması gereken bir durummuş gibi değerlendirilmiş, bu oldukça yanlıştır
#yapılan ürünün yorumunun yukarıda yer alıp yer almaması durumunu söyleyecek olan kullanıcıların kendisidir, kullanıcılar bunu faydalı buluyorsa bunlar yukarıda yer almalıdır.


comments.sort_values("wilson_lower_bound", ascending=False)


#önümüzde bir puan hesabı işi olduğunda şunları biliyorum; average alabilirim ama bunu daha fazla hassaslaştırabilirim örneğin zamana dayalı, user quality'e dayalı hassaslaştırma yapılabilir
#elimde 5 yıldızlı bir rating olduğunda bayesian_average_rating ile hesaplayabilirim
#hepsini bir araya getirip, hepsinin ağrılıını biçimlendirerek, birden fazla koşulu göz önünde bulundurarak hassaslaştırma yapılabilir


#sıralama da ele alınması gereken birden fazla faktör olduğu bilgisiydi bu faktörelere ağırlık vermek gerekiyordu
#göz önünde bulundurulması gereken durum --> ilgili probleme özel yazılmış kişisel bir matmatiksel çözümde olabilir (imdb'nin yaptığı gibi) kendileri matematiksel bir score üretme formülü geliştirmişler ve bunu kullanmışlardır
#bayesian score yöntemi puanların dağılım bilgisine göre olasılıksal bir ortalama hesaplıyordu


