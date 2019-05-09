import binascii

from Crypto.Util.number import inverse


# base ** secret = my_mix mod palette
class Solve:
    def __init__(self):
        self.palette = 2 ** 2048
        self.base = 13489305024865487703110255658234329747698118206959778644688156332043783846078839120693894255527894489531905012244713117142764166452312133019772171674466933769775907460046497284522592167536594047800489828714315435570429416637425443402332599055774982796405757075108551322778712959943658831605397635195107786224617525627358659165255604556424206194207190437525742567525338826878962081515333896433312311548844614323540250054093970082337500580573165008440265840792908334486258260848163001490152587781983042546491301026074736907693887630347258892882871059741621049169714319440564952700454580681894452760215968494428411686329
        self.my_mix = 6870295205307030503255600311283969014496436297715066273709495591567561187646528069669895230912327862244474990612611625088862250315706633708998214109152824455738719595737772769297517386968692628228327225922261219083693899105983726637012353264168761696183327692619506267951701511870035935612090359086376808592001973358166067468618577312983514388332736591060901174314042634365304017788649960016991442596975922402288221898367955532116456798868804571091463566329706023967280838744359633963847966790121312196824818606244189274966061324393424041211903396020720341163472399763951106703068172772579049891895580785347369093113
        self.your_mix = 14317253516668543276504878316838097235650210449758621543536146016892160048656997634541093315774403078357942150970695487937570449270120625898199254439189104072891595263513437420116930684308702803055295267600790477195902538538739117809573391251939794413361184343367694928615752045687223262368136262534778688889202144260002584306527206705616186699377315031757095455954292951059462279988296369935635246644221722025457496936215039008069820514166063271894671978845634968761626636993374291118230179892722513818307254406450607168911057458141649111515924404215975886422961651958216688209696158879621701708955382424640000048217
        self.painting = 17665922529512695488143524113273224470194093921285273353477875204196603230641896039854934719468650093602325707751566466034447988065494130102242572713515917910688574332104680867377750329904425039785453961697828887505197701127086732126907914324992806733394244034438537271953062873710421922341053639880387051921552573241651939698279628619278357238684137922164483956735128373164911380749908774512869223017256152942356111845682044048514917460601214157119487675633689081081818805777951203838578632029105960085810547586385599419736400861419214277678792284994133722491622512615732083564207280344459191773058670866354126043620
        self.secret = [0]

    # base ** n = 1 mod palette を見たす n を計算する
    def get_order_of_base(self):
        for n in range(2049):
            if pow(self.base, 2 ** n, 2 ** 2048) == 1:
                self.order_of_base = 2 ** n
                self.p = 2
                self.e = n
                break

    def get_pohlig_hellman(self):
        self.get_order_of_base()
        gamma = pow(self.base, self.p ** (self.e - 1), self.palette)
        for k in range(self.e):
            item = pow(inverse(self.base, self.palette), self.secret[k], self.palette) * self.my_mix % self.palette
            h_k = pow(item, pow(self.p, self.e - 1 - k), self.palette)
            d_k = 1 if gamma == h_k else 0
            self.secret.append(self.secret[k] + self.p ** k * d_k)
        return self.secret[-1]

    def get_flag(self):
        secret = self.get_pohlig_hellman()
        shared_mix = pow(self.your_mix, secret, self.palette)
        image = self.painting ^ shared_mix
        return binascii.unhexlify(hex(image)[2:])


if __name__ == '__main__':
    solve = Solve()
    print(solve.get_flag())
