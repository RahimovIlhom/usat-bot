# Response texts
RESPONSE_TEXTS = {
    'uz': {
        'draft': "❗️ Arizangiz hali tayyor emas. Iltimos, arizangizni yuboring.",
        'submitted': "❗️ Arizangiz yuborilgan. Iltimos, arizangiz qabul qilinishini kuting.",
        'rejected': ("😔 Afsuski, arizangiz tasdiqlanmadi. Iltimos, kiritgan ma’lumotlaringizni tekshirib, "
                     "yana boshqatdan yuboring."),
        'failed': ("Fan va texnologiyalar universitetining kirish imtihonlari tizimiga xush kelibsiz!\n"
                   "❗️ Siz imtihondan o'ta olmadingiz. Shuning uchun sizga yana imkoniyat berildi.\n\n"
                   "{} ta fandan umumiy {} ta test savollari uchun 4 soat vaqt beriladi."),
        'passed': ("🥳 Tabriklaymiz, siz Fan va texnologiyalar "
                   "universitetiga talabalikka tavsiya etildingiz! Shartnomani https://qabul.usat.uz saytidagi "
                   "shaxsiy kabinetdan yuklab olishingiz mumkin. Saytga kirish uchun parol sizga SMS xabar sifatida "
                   "yuborilgan. Savollaringiz bo’lsa bizga qo’ng’iroq qiling: 78-888-38-88"),
        'examined': ("✅ Siz imtihon topshirib bo'lgansiz!\n"
                     "Imtihon natijangizni «👤 Profilim» ning «📊 Imtihon natijam» bo'limida ko'rishingiz mumkin."),
        'no_exam_questions': "❗️ Hozirda imtihon savollari mavjud emas!",
        'welcome_message': ("Fan va texnologiyalar universitetining kirish imtihonlari tizimiga xush "
                            "kelibsiz!\n{} ta fandan umumiy {} ta test savollari uchun 4 soat vaqt beriladi."),
        'need_application': "❗️ Imtihon topshirish uchun avval universitetga hujjat topshirishingiz kerak!",
        'two_failed': "Siz ikkinchi imkoniyatda ham imtihondan o'ta olmagansiz!",
        'error': "😬 Noma'lum xatolik!",
        'time_up': "❗️ Imtihon uchun berilgan 4 soat vaqt yakunlandi.",
    },
    'ru': {
        'draft': "❗️ Ваша заявка еще не готова. Пожалуйста, отправьте вашу заявку.",
        'submitted': "❗️ Ваша заявка отправлена. Пожалуйста, ожидайте подтверждения вашей заявки.",
        'rejected': ("😔 К сожалению, ваша заявка не была подтверждена. Пожалуйста, проверьте введенные данные и "
                     "отправьте их снова."),
        'failed': ("Добро пожаловать в систему вступительных экзаменов Университета науки и технологий!\n"
                   "❗️ Вы не прошли экзамен. Поэтому вам предоставляется еще одна возможность.\n\n"
                   "Для {} предметов выделено 4 часа на общий {} вопросов."),
        'passed': ("🥳 Поздравляем, вас рекомендовали к зачислению в Университет науки и технологий! Вы можете "
                   "скачать договор из личного кабинета на сайте https://qabul.usat.uz. Пароль для входа на сайт был "
                   "отправлен вам в SMS-сообщении. Если у вас есть вопросы, позвоните нам: 78-888-38-88"),
        'examined': ("✅ Вы сдали экзамен!\n"
                     "Ваши результаты экзамена можно посмотреть в разделе «👤 Мой профиль» -> «📊 Мои "
                     "результаты экзамена»."),
        'no_exam_questions': "❗️ В настоящее время экзаменационные вопросы отсутствуют!",
        'welcome_message': (
            "Добро пожаловать в систему вступительных экзаменов Университета науки и технологий!\n"
            "Для {} предметов выделено 4 часа на общий {} вопросов."),
        'need_application': "❗️ Для сдачи экзамена необходимо сначала подать документы в университет!",
        'two_failed': "Вы не смогли сдать экзамен даже со второй попытки!",
        'error': "😬 Неизвестная ошибка!",
        'time_up': "❗️ Для экзамена отведенные 4 часа завершились.",
    }
}

INFORMATION_TEXTS = {
    'uz': ("Universitetga hujjatlarni ham, imtihonni ham onlayn topshirishni istaysizmi? Grant asosida ta'lim "
           "olishni, stipendiya olishni xohlaysizmi? Oliy ta’limni nufuzli va zamonaviy universitetda "
           "olmoqchimisiz? Sifatli ta'lim, individual yondashuv va rivojlanish uchun keng imkoniyatlar taklif "
           "qiladigan universitetni izlayapsizmi? Unday bo’lsa siz e’tiboringizni O’zbekistondagi eng yaxshi "
           "universitetlardan biri bo’lgan Fan va texnologiyalar universitetiga qaratishingiz lozim.\n\nFan va "
           "texnologiyalar universiteti O‘zbekiston Respublikasi Vazirlar Mahkamasi huzuridagi Taʼlim sifatini "
           "nazorat qilish davlat inspeksiyasi tomonidan 2022-yil 27-iyul kuni berilgan № 048714 litsenziyasi "
           "asosida mamlakatda o’z faoliyatini yuritadi.\n\nUniversitet o’z faoliyatini 2022-yilda boshlaganiga "
           "qaramay, hozirda universitetda 5000 dan ortiq talaba tahsil olmoqda, ularga 100 ga yaqin malakali "
           "professor-o’qituvchilar sifatli ta’lim berib kelmoqda.\n\nUniversitetimiz yosh bo'lishiga qaramay, "
           "hozirdan yuqori marralarni egallamoqda. Masalan, 2023-yil dekabr oyida talabalarimiz 135 ta OTM "
           "jamoalari, shu jumladan 1080 nafar talaba ishtirok etgan “Zakovat” intellektual olimpiadasining "
           "respublika bosqichida 1-o’rinni qo’lga kiritdi va 2 mlrd so’m miqdoridagi Prezident sovg’asi bilan "
           "taqdirlandi.\n\nBatafsil 👉 [Ko'p soraladigan savollarga javoblar]"
           "(https://telegra.ph/Kop-soraladigan-savollarga-javoblar-07-25)"),
    'ru':
        ("Хотите подать документы и сдать экзамен онлайн в университет? Хотите учиться на гранте и получать "
         "стипендию? Хотите получить высшее образование в престижном и современном университете? Ищете "
         "университет, предлагающий качественное образование, индивидуальный подход и широкие возможности для "
         "развития? Тогда вам стоит обратить внимание на один из лучших университетов Узбекистана – Университет "
         "наук и технологий.\n\nУниверситет наук и технологий осуществляет свою деятельность на основании лицензии "
         "№ 048714, выданной Государственной инспекцией по контролю качества образования при Кабинете Министров "
         "Республики Узбекистан 27 июля 2022 года.\n\nНесмотря на то, что университет начал свою деятельность в "
         "2022 году, в настоящее время в университете обучаются более 5000 студентов, которым качественное образование "
         "предоставляют около 100 квалифицированных преподавателей.\n\nНесмотря на молодость нашего университета, "
         "он уже достигает высоких результатов. Например, в декабре 2023 года наши студенты заняли 1-е место в "
         "республиканском этапе интеллектуальной олимпиады «Заковат» среди 135 команд вузов, включая 1080 студентов, "
         "и были награждены президентским подарком в размере 2 млрд сумов.\n\n"
         "Подробности 👉 [Ответы на часто задаваемые вопросы]"
         "(https://telegra.ph/Kop-soraladigan-savollarga-javoblar-07-25)")
}

DIRECTIONS_EDU = {
    'uz': ["Logistika", "Maktabgacha ta’lim", "Boshlang’ich ta’lim", "Tarix", "Xorijiy til va adabiyoti", "Iqtisodiyot",
           "Psixologiya", "Buxgalteriya hisobi va audit", "Moliya va moliyaviy texnologiyalar", "Bank ishi va auditi",
           "Dasturiy injiniring", "Turizm"],
    'ru': ["Логистика", "Дошкольное образование", "Начальное образование", "История", "Иностранный язык и литература",
           "Экономика", "Психология", "Бухгалтерский учет и аудит", "Финансы и финансовые технологии",
           "Банковское дело и аудит", "Программная инженерия", "Туризм"]
}

DIRECTIONS_EDU_INFO_UZ = {
    "Logistika": {
        'image': "http://telegra.ph//file/e80dcf617ee497b81bc79.jpg",
        "Yo’nalish haqida ma’lumot": "Logistika - biznesning samarali ishlashining asosiy mezonlaridan biridir. Ushbu sohada o'qish talabalarga butun dunyo bo'ylab mahsulotlarni yetkazib berish, saqlash va tarqatish bilan bog'liq jarayonlar haqida global tushunchani shakllantirish imkonini beradi.\nBugungi kunda logistika strategik muhim soha bo'lib, unda talabalar mahsulotlar va ma'lumotlar oqimini samarali boshqarishni o'rganadilar. Ular, shuningdek, ta'minot zanjirlarini optimallashtirish, inventarizatsiyani boshqarish va tovarlarni tashish va taqsimlashni muvofiqlashtirish usullari haqida ham bilimga ega bo’lishadi.\nO'qishni tugatgandan so'ng, logistika bo'yicha ixtisoslashgan talabalar turli biznes sohalarida ishlashlari mumkin. Jumladan, ekspeditorlik, transport, yuklarni tashish, saqlash va qadoqlash kompaniyalarida logistika jarayonlarining samarali ishlashini ta'minlovchi logistika menejerlari, ta'minot koordinatorlari va ta'minot zanjiri tahlilchilari sifatida kuchli mutaxassis bo’lishlari mumkin.\nLogistik mutaxassislarga talabning ortishi O’zbekistonda yirik logistika markazlari va ko'p maqsadli omborlar qurilishining avj olishi, shuningdek, xalqaro bozorlar munosabarlarining rivojlanishi bilan bog'liq.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 100\nKechki:100\nSirtqi:300\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:50",
        "Qabul qilinish talablari": "Matematika – 3,1 ball\n(25 ta savol)\n\nIngliz tili – 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Maktabgacha ta’lim": {
        "image": "http://telegra.ph//file/c555fd38b7b47d1944f33.jpg",
        "Yo’nalish haqida ma’lumot": "Maktabgacha ta’lim - bu talabalarni yosh bolalar bilan ishlashga tayyorlaydigan soha. O‘quv jarayonida talabalar maktab yoshiga yetmagan bolalarga ta’lim berish usullarini, bolalar psixologiyasini o‘rganadilar, ota-onalar bilan muloqot qilish ko‘nikmalarini rivojlantiradilar.\n'Maktabgacha ta'lim' yo'nalishini tamomlagan talabalar bog'chalarda o'qituvchi, tarbiyachi va erta rivojlanish sohasidagi mutaxassislar bo'lishlari mumkin. Shuningdek, ular ota-onalarga yordam ko'rsatish va maktabgacha ta'lim muassasalari uchun ta'lim dasturlarini ishlab chiqishda maslahatchi sifatida ham ishlashlari mumkin.\nBolalar bilan erta yoshda ishlash ularning rivojlanishiga katta hissa qo'shish imkoniyatini beradi. Erta yoshdagi bolalar ta'limi mutaxassislari bolalarda bilim, ijtimoiy ko'nikmalar va hissiy intellekt asoslarini yaratadilar va shu bilan ularning kelajagiga ijobiy ta'sir ko'rsatadilar.\nO’zbekistonda maktabgacha ta'limga qiziqish ortib bormoqda, bu esa malakali mutaxassislarga talabni oshiradi.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 100\nKechki:100\nSirtqi:600\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:50",
        "Qabul qilinish talablari": "Ona tili va adabiyot – 3,1 ball\n(25 ta savol)\n\nMatematika – 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Boshlang’ich ta’lim": {
        "image": "http://telegra.ph//file/09f2e8799b388506caec3.jpg",
        "Yo’nalish haqida ma’lumot": "'Boshlang‘ich ta’lim' yo‘nalishida talabalar boshlang‘ich sinflarda bolalar bilan ishlash bo‘yicha asosiy bilim va uslublarni o’rganadi. O’qish davomida talabalar pedagogika tamoyillarini, asosiy fanlarni o'qitish metodlarini o'rganadilar, shuningdek, o'quv jarayonini tashkillashtirish va o’quvchilar bilan muloqot qilish ko'nikmalarini egallaydilar.\n'Boshlang‘ich ta’lim' yo‘nalishi bo‘yicha oliy ma’lumotga ega bo‘lganlar boshlang‘ich sinf o‘qituvchilari, maktabdan tashqari ishlar tashkilotchisi, shuningdek, maktabgacha ta’limni rivojlantirish bo‘yicha mutaxassis bo‘lishlari mumkin. Shuningdek, ular o'z bilimlarini ta'lim bo'yicha maslahatchilar sifatida hamda ta'lim dasturlarini ishlab chiqishda qo'llashlari mumkin.\nAytib o’tish lozim, boshlang'ich sinf - bu bolaning hayotidagi asosiy ko'nikmalar, qadriyatlar va bilim olishga bo'lgan munosabati shakllanadigan asosiy davrdir. Boshlang'ich ta'lim mutaxassislari har bir bolaning shaxsiy rivojlanishiga sezilarli ta'sir ko'rsatadi.\nBolalar bilan ishlash ijodkorlik va innovatsiyalarni talab qiladi. Boshlang‘ich sinf o‘qituvchilari o‘quv jarayonini qiziqarli va samarali o‘tkazish uchun o‘qitishning turli usullaridan, jumladan, o‘yin va interfaol darslardan foydalanadilar.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 300\nKechki:100\nSirtqi:50\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:50",
        "Qabul qilinish talablari": "Ona tili va adabiyot – 3,1 ball\n(25 ta savol)\n\nMatematika – 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Tarix": {
        "image": "http://telegra.ph//file/5467d9e94197c52a420dd.jpg",
        "Yo’nalish haqida ma’lumot": "'Tarix' yo‘nalishi talabalarni o‘tmishning qiziqarli jabhalarini o‘rganishga chorlab, ularga vaqt sirlarini ochish va dunyoni shakllantirgan muhim voqealarni tushunish imkonini beradi. O‘qish davomida talabalar tarixiy tahlil usullarini o‘zlashtiradilar, o‘tmishdagi madaniy va ijtimoiy sharoitlarni o‘rganadilar, tanqidiy fikrlashni rivojlantiradilar.\n'Tarix' yo‘nalishini tamomlaganlar o‘z faoliyatini ta’lim muassasalarida tarix o‘qituvchisi, arxiv mutaxassisi, muzey xodimlari, tarixiy mavzularga ixtisoslashgan jurnalist sifatida boshlashlari mumkin bo’ladi.\nTarix o'tmishni chuqur tushunish, tanqidiy fikrlashni rivojlantirish va qadriyatlarni rivojlantirish imkoniyatini beradi, bu esa ushbu sohani juda muhim va qadrli ekanligini dasdiqlaydi.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 100\nKechki:100\nSirtqi:200\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:50",
        "Qabul qilinish talablari": "Tarix – 3,1 ball\n(25 ta savol)\n\nIngliz tili– 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Xorijiy til va adabiyoti": {
        "image": "http://telegra.ph//file/6c430925fe882b39351f4.jpg",
        "Yo’nalish haqida ma’lumot": "'Xorijiy til va adabiyoti' yo‘nalishi talabalarga xorijiy til, adabiy asarlar va madaniy jihatlar haqida chuqur tushuncha beradi. O‘quv jarayonida talabalar tarjima, adabiy tahlil va madaniyatlararo muloqot ko‘nikmalarini egallaydi, bu esa ularning madaniy boyligi va lingvistik tajribasini shakllantiradi.\n'Xorijiy til va adabiyoti' yoʻnalishida taʼlim olgan bitiruvchilar chet tili oʻqituvchisi, tarjimon, adabiyotshunos, muharrir va hatto diplomat boʻlishlari mumkin. Shuningdek, ular xalqaro kompaniyalarda, turizm sohasida, jurnalistikada va xalqaro aloqalarda kasb egallashlari mumkin, bu sohalarda ularning xorijiy til va madaniyatni bilishi muhim bo'ladi.\nChet tilini bilish global fikrlashni rivojlantirishga va turli nuqtai nazarlarni tushunishga yordam beradi. Bu, ayniqsa, hozirgi globallashuv davrida juda muhimdir. Shu bilan birga, ko'pgina xorijiy kompaniyalar bir nechta tillarda muloqot qila oladigan xodimlarni qadrlashadi.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 200\nKechki:100\nSirtqi:yo'q\n\nRus\nKunduzgi: 100\nKechki:50\nSirtqi:yo'q",
        "Qabul qilinish talablari": "Ingliz tili – 3,1 ball\n(25 ta savol)\n\nOna tili va adabiyot– 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Iqtisodiyot": {
        "image": "http://telegra.ph//file/4debc259a7e185fda3fd5.jpg",
        "Yo’nalish haqida ma’lumot": "'Iqtisodiyot' yo‘nalishi talabalarga moliya, makro va mikroiqtisodiyot, shuningdek, iqtisodiy jarayonlarni tahlil qilish usullari bo‘yicha chuqur bilimlar beradi. O’qish davomida talabalar bozor tahlili tamoyillarini o‘rganadilar, biznesda strategik qarorlar qabul qilish ko‘nikmalarini rivojlantiradilar.\nIqtisodiyot fakulteti bitiruvchilari moliya, bank ishi, loyihalarni boshqarish, konsalting va boshqa ko'plab sohalarda ishlashlari mumkin. Ular moliyaviy tahlilchi, buxgalteriya menejeri, iqtisodchi bo'lishlari, shuningdek, audit va soliq maslahati bilan shug'ullanishlari mumkin. Davlat boshqaruvi yoki xalqaro tashkilotlar sohasida ham bitiruvchilarning iqtisodiy bilimlarini qo‘llash uchun keng imkoniyatlar mavjud.\nShu bilan birga, iqtisodiyot bo’yicha mutaxassislar o’z bilimlarini biror biznesni boshlash va boshqarish uchun qo’llashlari mumkin. Bu tadbirkorlik uchun qulay imkoniyatlarni yaratadi.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 100\nKechki:100\nSirtqi:400\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:50",
        "Qabul qilinish talablari": "Matematika – 3,1 ball\n(25 ta savol)\n\nIngliz tili– 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Psixologiya": {
        "image": "http://telegra.ph//file/1371c84abd713df72e376.jpg",
        "Yo’nalish haqida ma’lumot": "'Psixologiya' yo‘nalishi talabalarga inson ruhiyati, emotsional holati va xulq-atvorga ta’sir qilish usullari haqida chuqur bilim beradi. Talabalar o'qish davomida psixologik nazariyalarni, tadqiqot usullarini, shuningdek, psixologik muammolarni hal qilishda maslahat va yordam berish ko'nikmalarini o'rganadilar.\nPsixologiya bo’yicha mutaxassislar klinik psixologiya, ta'lim, kadrlar boshqaruvi, marketing, tadqiqot va hatto sport psixologiyasi kabi turli sohalarda ishlashlari mumkin. Ular amaliyotchi psixoterapevt, maktab psixologi, inson resurslari bo'yicha maslahatchi, marketolog yoki psixologiya bo'yicha tadqiqotchi bo'lib, inson xatti-harakatlarini tushunishga hissa qo'shishi mumkin.\nShu bilan birga, psixologlar hissiy qiyinchiliklar, stress, depressiya va boshqa muammolarga duch kelgan odamlarga yordam berishlari mumkin.\nUmuman olganda 'psixologiya' yo‘nalishida o'qish hayotning turli sohalarida foydali bo'lishi mumkin bo'lgan keng ko'lamli ko'nikma va bilimlarni beradi, bu esa ko'plab talabalar uchun ushbu ta'lim sohasini jozibador qiladi.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 100\nKechki:100\nSirtqi:600\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:50",
        "Qabul qilinish talablari": "Biologiya – 3,1 ball\n(25 ta savol)\n\nOna tili– 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Buxgalteriya hisobi va audit": {
        "image": "http://telegra.ph//file/2b2f95aa7d1623e5ea630.jpg",
        "Yo’nalish haqida ma’lumot": "'Buxgalteriya hisobi va audit' yo‘nalishi talabalarga moliyaviy hisob, soliq va audit sohalarida chuqur bilim beradi. O’qish davomida talabalar moliyaviy hisobot usullarini, ichki nazorat tamoyillarini o'rganadilar, shuningdek, buxgalteriya hisobi qonunchiligini o'rganadilar.\nBuxgalteriya hisobi va audit bo'yicha bilimga ega bo'lgan bitiruvchilar buxgalter, auditor, moliyaviy tahlilchi yoki soliq mutaxassisi bo'lishlari mumkin. Ular, shuningdek, ichki auditorlar, moliyaviy rejalashtirish bo'yicha maslahatchilar lavozimlarini egallashlari mumkin. Moliyaviy institutlar, korporatsiyalar va konsalting kompaniyalarida ishlash imkoniyati ham bitiruvchilar uchun keng istiqbollarni ochadi.\nBuxgalterlar va auditorlar har qanday biznesda asosiy rolni o'ynaydi. Buxgalteriya hisobi va audit bo'yicha mutaxassislarga talab doimo yuqori bo'lib, bu, o’z navbatida, ushbu kasbni barqaror va talabgir qiladi.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 100\nKechki:100\nSirtqi:400\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:50",
        "Qabul qilinish talablari": "Matematika – 3,1 ball\n(25 ta savol)\n\nIngliz tili– 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Moliya va moliyaviy texnologiyalar": {
        "image": "http://telegra.ph//file/f866e91f8dcc454a6e2b4.jpg",
        "Yo’nalish haqida ma’lumot": "'Moliya va moliyaviy texnologiyalar' yo‘nalishi talabalarga moliya sohasida chuqur bilim beradi, shuningdek, moliya sohasida qo‘llaniladigan zamonaviy texnologiyalar bilan tanishtiradi. O’qish davomida talabalar moliyaviy tahlil, investitsiyalarni boshqarish usullarini o'rganadilar, shuningdek, moliyaviy vositalar va texnologik yechimlar bilan ishlash ko'nikmalarini egallaydilar.\nMoliya va moliyaviy texnologiyalar mutaxassisliklari bo'yicha bitiruvchilar faoliyatini korporativ moliya, investitsiyalar, moliyaviy tahlil kabi turli sohalarda va moliyaviy-texnologiyaviy startaplarda davom ettirishlari mumkin. Ular moliyaviy konsalting kompaniyalarida ishlash, moliyaviy dasturlarni ishlab chiqish va moliyaviy jarayonlarga innovatsion texnologiyalarni joriy etish bilan shug'ullanishlari mumkin.\nMoliya sohasi, ayniqsa, yangi texnologiyalarni joriy etilayotganini hisobga olgan holda doimiy ravishda rivojlanib bormoqda. Bu talabalarga dinamik va istiqbolli sohada ishlash imkoniyatini beradi.\nUshbu yo'nalishda ta’lim olish moliyaviy menejment, shuningdek, moliyaviy texnologiyalar, jumladan, blokcheyn, sun'iy intellekt va raqamli to'lovlar bo'yicha maxsus ko'nikmalarga ega bo’lishga imkon beradi.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 250\nKechki:100\nSirtqi:1000\n\nRus\nKunduzgi: 100\nKechki:50\nSirtqi:150",
        "Qabul qilinish talablari": "Matematika – 3,1 ball\n(25 ta savol)\n\nIngliz tili– 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Bank ishi va auditi": {
        "image": "http://telegra.ph//file/562a1ee48a607eb111210.jpg",
        "Yo’nalish haqida ma’lumot": "'Bank ishi va audit' yo‘nalishi talabalarga bank ishi, moliyaviy audit va risklarni boshqarish bo‘yicha chuqur bilim beradi. O’qish davomida talabalar banklarning ishlash tamoyillari, moliyaviy audit usullarini o'rganadilar, shuningdek, moliyaviy risklarni baholash va boshqarish tamoyillarini o'zlashtiradilar.\n'Bank ishi va audit' ixtisosligi bo‘yicha bitiruvchilar bank sohasida ishlashni davom ettirishlari mumkin, moliyaviy auditorlar, risk menejerlari yoki korporativ moliya bo‘yicha mutaxassis bo‘lishlari mumkin. Shuningdek, ular konsalting, boylikni boshqarish, kompaniyalarning moliyaviy bo'limlarida ishlash yoki moliya sohasida audit va konsalting bo'yicha kasb tanlashlari mumkin.\nNima uchun 'Bank ishi va audit' yo’nalishini tanlash kerak? Bank sektori doimiy ravishda o'sib, rivojlanib, yangi ish o‘rinlari va yangi imkoniyatlarni yaratmoqda. Zamonaviy texnologiyalar va moliya sohasidagi o'zgarishlar ushbu yo’nalishni ayniqsa talabgir qilmoqda. Malakali bank va audit mutaxassislari moliyaviy barqarorlikni ta'minlash va iqtisodiy noaniqlik davrida risklarni kamaytirishga yordam beradi. Ushbu sohadagi mutaxassislar hozirgi kunda milliy va xalqaro miqyosda katta talabga ega.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 200\nKechki:100\nSirtqi:1000\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:100",
        "Qabul qilinish talablari": "Matematika – 3,1 ball\n(25 ta savol)\n\nIngliz tili– 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Dasturiy injiniring": {
        "image": "http://telegra.ph//file/91e10743020695f5cf596.jpg",
        "Yo’nalish haqida ma’lumot": "'Dasturiy injiniring' yo'nalishi talabalarga dasturiy ta'minotni ishlab chiqish, kompyuter tizimlari arxitekturasi va dasturlash metodologiyasi bo'yicha chuqur bilim beradi. O’qish davomida talabalar turli dasturlash tillarini puxta egallaydi, algoritmlarni tahlil qiladi, zamonaviy ishlanma texnologiyalarini o‘rganadi.\nDasturiy ta'minot muhandisligi darajasiga ega bo'lgan bitiruvchilar axborot texnologiyalari sohasida dasturchi, dasturiy ta'minot ishlab chiquvchisi, tizim tahlilchisi yoki tester sifatida ishlashni boshlashlari mumkin. Shuningdek, ular ilmiy-tadqiqot va ishlanmalarda, innovatsion dasturiy mahsulotlar yaratish sohalarida kasb tanlashlari mumkin. Shuningdek, bitiruvchilar texnologik startaplarda, ilovalarni ishlab chiqish kompaniyalarida, sun'iy intellekt va mashinaviy o'rganish bo'yicha kompaniyalarda ham ishlashlari mumkin bo’ladi.\nRaqamli transformatsiya va axborot texnologiyalarining ahamiyati ortib borayotgan sharoitda malakali dasturchilarga bo‘lgan ehtiyoj tez sur’atlar bilan o‘sib bormoqda. Sun'iy intellekt, mashinali o'rganish va katta ma'lumotlar kabi zamonaviy texnologiyalar murakkab dasturiy yechimlarni ishlab chiqa oladigan va ularga xizmat ko'rsatadigan mutaxassislarni talab qiladi. Dasturiy injiniring ilg'or sohalarda ishlash uchun zarur bo'lgan bilim va ko'nikmalarni beradi, bu uni juda dolzarb va istiqbolli sohaga aylantiradi.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 150\nKechki:100\nSirtqi:150\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:50",
        "Qabul qilinish talablari": "Matematika – 3,1 ball\n(25 ta savol)\n\nIngliz tili– 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    },
    "Turizm": {
        "image": "http://telegra.ph//file/c9b1988cffa2a4a2547e1.jpg",
        "Yo’nalish haqida ma’lumot": "'Turizm' yo‘nalishi talabalarga turizm xizmatlarini tashkil etish va boshqarish, milliy va xalqaro turizm sohalarida chuqur bilim beradi. O’qish davomida talabalar mehmondo‘stlik asoslari, turizm marketingi va turizm biznesini boshqarishning turli jihatlarini o‘rganadilar.\nTurizm bo'yicha diplomga ega bo'lgan bitiruvchilar mehmonxona sanoatida, turoperatorlarda, tadbir agentliklarida va hatto turizm bilan bog'liq madaniyat muassasalarida ish topishlari mumkin. Ular turizm menejeri, ekskursiya gidlari, turistik marshrutlarni ishlab chiqish bo'yicha mutaxassis bo'lishlari yoki xalqaro turizm bilan shug'ullanishlari mumkin. Bundan tashqari, bitiruvchilar turizm bo'yicha konsalting, tadbirlarni boshqarish bo'yicha kasb tanlashi yoki turizm sohasida o'z tadbirkorligini boshlashi mumkin.\nZamonaviy turizm globallashuv, xalqaro sayohatlarning o'sishi va sayyohlik yo'nalishlari sonining ko'payishi tufayli faol rivojlanmoqda. Turizm industriyasi pandemiyadan keyin tiklanib, yangi sharoitlarga moslashib, innovatsion yechimlarni joriy eta oladigan va yuqori darajadagi xizmat ko‘rsata oladigan mutaxassislar uchun noyob imkoniyatlarni taklif qilmoqda. Turizm hududlarning iqtisodiy rivojlanishiga, madaniy aloqalarni mustahkamlashga va hayot sifatini yaxshilashga xizmat qiladi, bu esa uni dolzarb va istiqbolli yo‘nalishga aylantiradi.",
        "2024/2025-yil uchun qabul kvotasi": "O'zbek\nKunduzgi: 150\nKechki:100\nSirtqi:400\n\nRus\nKunduzgi: 50\nKechki:50\nSirtqi:100",
        "Qabul qilinish talablari": "Tarix – 3,1 ball\n(25 ta savol)\n\nIngliz tili– 2,1 ball\n(25 ta savol)\n\nMantiqiy savol – 1,1 ball\n(10 ta savol)"
    }
}

DIRECTIONS_EDU_INFO_RU = {
    "Логистика": {
        'image': "http://telegra.ph//file/e80dcf617ee497b81bc79.jpg",
        "Информация о направлении": "Логистика - один из ключевых критериев эффективного функционирования бизнеса. Обучение в этой области дает студентам возможность сформировать глобальное представление о процессах, связанных с доставкой, хранением и распределением продуктов по всему миру.\nСегодня логистика является стратегически важной областью, в которой студенты изучают эффективное управление потоками продуктов и информации. Они также приобретают знания о методах оптимизации цепочек поставок, управления запасами и координации транспортировки и распределения товаров.\nПосле завершения обучения студенты, специализирующиеся на логистике, могут работать в различных сферах бизнеса. Включая компании по экспедированию, транспортировке, перевозке, хранению и упаковке грузов, где они могут стать логистическими менеджерами, координаторами поставок и аналитиками цепочек поставок.\nРост спроса на логистических специалистов связан с активным строительством крупных логистических центров и многоцелевых складов в Узбекистане, а также с развитием международных рыночных отношений.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 100\nВечернее: 100\nЗаочное: 300\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 50",
        "Требования к поступлению": "Математика – 3,1 балла\n(25 вопросов)\n\nАнглийский язык – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Дошкольное образование": {
        "image": "http://telegra.ph//file/c555fd38b7b47d1944f33.jpg",
        "Информация о направлении": "Дошкольное образование - это область, готовящая студентов к работе с маленькими детьми. В процессе обучения студенты изучают методы обучения детей дошкольного возраста, детскую психологию, развивают навыки общения с родителями.\nВыпускники направления 'Дошкольное образование' могут стать воспитателями, педагогами и специалистами по раннему развитию в детских садах. Они также могут работать консультантами, оказывающими помощь родителям и разрабатывающими образовательные программы для дошкольных учреждений.\nРабота с детьми в раннем возрасте позволяет вносить значительный вклад в их развитие. Специалисты по раннему детскому образованию закладывают основы знаний, социальных навыков и эмоционального интеллекта у детей, что оказывает положительное влияние на их будущее.\nВ Узбекистане интерес к дошкольному образованию растет, что увеличивает спрос на квалифицированных специалистов.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 100\nВечернее: 100\nЗаочное: 600\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 50",
        "Требования к поступлению": "Родной язык и литература – 3,1 балла\n(25 вопросов)\n\nМатематика – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Начальное образование": {
        "image": "http://telegra.ph//file/09f2e8799b388506caec3.jpg",
        "Информация о направлении": "'Начальное образование' направлено на обучение студентов основным методам и знаниям, необходимым для работы с детьми начальных классов. В процессе обучения студенты изучают принципы педагогики, методы преподавания основных предметов, а также приобретают навыки организации учебного процесса и общения с учениками.\nВыпускники направления 'Начальное образование' могут стать учителями начальных классов, организаторами внеклассных мероприятий, а также специалистами по развитию дошкольного образования. Они также могут применять свои знания в качестве образовательных консультантов и разработчиков образовательных программ.\nНачальная школа - это ключевой период, когда у ребенка формируются основные навыки, ценности и отношение к учебе. Специалисты по начальному образованию оказывают значительное влияние на личное развитие каждого ребенка.\nРабота с детьми требует творчества и инноваций. Учителя начальных классов используют различные методы обучения, включая игры и интерактивные занятия, чтобы сделать учебный процесс интересным и эффективным.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 300\nВечернее: 100\nЗаочное: 50\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 50",
        "Требования к поступлению": "Родной язык и литература – 3,1 балла\n(25 вопросов)\n\nМатематика – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "История": {
        "image": "http://telegra.ph//file/5467d9e94197c52a420dd.jpg",
        "Информация о направлении": "'История' приглашает студентов изучать увлекательные аспекты прошлого, дает им возможность раскрыть тайны времени и понять важные события, сформировавшие мир. В процессе обучения студенты осваивают методы исторического анализа, изучают культурные и социальные условия прошлого, развивают критическое мышление.\nВыпускники направления 'История' могут начать свою карьеру в образовательных учреждениях в качестве учителей истории, архивистов, музейных работников или журналистов, специализирующихся на исторических темах.\nИзучение истории позволяет глубже понять прошлое, развить критическое мышление и ценности, что делает эту область очень важной и ценной.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 100\nВечернее: 100\nЗаочное: 200\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 50",
        "Требования к поступлению": "История – 3,1 балла\n(25 вопросов)\n\nАнглийский язык – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Иностранный язык и литература": {
        "image": "http://telegra.ph//file/6c430925fe882b39351f4.jpg",
        "Информация о направлении": "'Иностранный язык и литература' дает студентам глубокое понимание иностранного языка, литературных произведений и культурных аспектов. В процессе обучения студенты осваивают перевод, литературный анализ и навыки межкультурного общения, что формирует их культурное богатство и лингвистический опыт.\nВыпускники направления 'Иностранный язык и литература' могут стать учителями иностранного языка, переводчиками, литературоведами, редакторами и даже дипломатами. Они могут работать в международных компаниях, в сфере туризма, журналистике и международных отношениях, где их знание иностранного языка и культуры будет очень ценным.\nЗнание иностранного языка способствует развитию глобального мышления и пониманию различных точек зрения. Это особенно важно в современную эпоху глобализации. Многие международные компании ценят сотрудников, способных общаться на нескольких языках.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 200\nВечернее: 100\nЗаочное: нет\n\nРусский\nОчное: 100\nВечернее: 50\nЗаочное: нет",
        "Требования к поступлению": "Английский язык – 3,1 балла\n(25 вопросов)\n\nРодной язык и литература – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Экономика": {
        "image": "http://telegra.ph//file/4debc259a7e185fda3fd5.jpg",
        "Информация о направлении": "'Экономика' дает студентам глубокие знания в области финансов, макро- и микроэкономики, а также методы анализа экономических процессов. В процессе обучения студенты изучают принципы рыночного анализа, развивают навыки стратегического принятия решений в бизнесе.\nВыпускники факультета экономики могут работать в области финансов, банковского дела, управления проектами, консалтинга и других сферах. Они могут стать финансовыми аналитиками, менеджерами бухгалтерского учета, экономистами, а также заниматься аудитом и налоговым консультированием. В государственном управлении или международных организациях также есть широкие возможности для применения их экономических знаний.\nКроме того, специалисты в области экономики могут использовать свои знания для создания и управления собственным бизнесом, что создает благоприятные возможности для предпринимательства.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 100\nВечернее: 100\nЗаочное: 400\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 50",
        "Требования к поступлению": "Математика – 3,1 балла\n(25 вопросов)\n\nАнглийский язык – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Психология": {
        "image": "http://telegra.ph//file/1371c84abd713df72e376.jpg",
        "Информация о направлении": "'Психология' дает студентам глубокие знания о психике человека, эмоциональном состоянии и способах воздействия на поведение. В процессе обучения студенты изучают психологические теории, методы исследования, а также развивают навыки консультирования и помощи в решении психологических проблем.\nСпециалисты в области психологии могут работать в клинической психологии, образовании, управлении персоналом, маркетинге, исследованиях и даже в спортивной психологии. Они могут стать практикующими психотерапевтами, школьными психологами, консультантами по управлению человеческими ресурсами, маркетологами или исследователями психологии, внося вклад в понимание человеческого поведения.\nКроме того, психологи могут помогать людям, сталкивающимся с эмоциональными трудностями, стрессом, депрессией и другими проблемами.\nВ целом, обучение по направлению 'психология' дает широкий спектр навыков и знаний, которые могут быть полезны в различных сферах жизни, что делает эту образовательную область привлекательной для многих студентов.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 100\nВечернее: 100\nЗаочное: 600\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 50",
        "Требования к поступлению": "Биология – 3,1 балла\n(25 вопросов)\n\nРодной язык – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Бухгалтерский учет и аудит": {
        "image": "http://telegra.ph//file/2b2f95aa7d1623e5ea630.jpg",
        "Информация о направлении": "'Бухгалтерский учет и аудит' дает студентам глубокие знания в области финансового учета, налогообложения и аудита. В процессе обучения студенты изучают методы финансовой отчетности, принципы внутреннего контроля, а также законодательство в области бухгалтерского учета.\nВыпускники с знаниями в области бухгалтерского учета и аудита могут стать бухгалтерами, аудиторами, финансовыми аналитиками или налоговыми специалистами. Они также могут занимать должности внутренних аудиторов, консультантов по финансовому планированию. Возможности трудоустройства в финансовых институтах, корпорациях и консалтинговых компаниях также открывают широкие перспективы для выпускников.\nБухгалтеры и аудиторы играют ключевую роль в любом бизнесе. Спрос на специалистов по бухгалтерскому учету и аудиту всегда высок, что делает эту профессию стабильной и востребованной.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 100\nВечернее: 100\nЗаочное: 400\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 50",
        "Требования к поступлению": "Математика – 3,1 балла\n(25 вопросов)\n\nАнглийский язык – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Финансы и финансовые технологии": {
        "image": "http://telegra.ph//file/f866e91f8dcc454a6e2b4.jpg",
        "Информация о направлении": "'Финансы и финансовые технологии' дает студентам глубокие знания в области финансов, а также знакомит с современными технологиями, применяемыми в финансовой сфере. В процессе обучения студенты изучают методы финансового анализа, управления инвестициями, а также приобретают навыки работы с финансовыми инструментами и технологическими решениями.\nВыпускники, специализирующиеся в области финансов и финансовых технологий, могут продолжить свою карьеру в корпоративных финансах, инвестициях, финансовом анализе и стартапах в сфере финансовых технологий. Они могут работать в консалтинговых компаниях, разрабатывать финансовые программы и внедрять инновационные технологии в финансовые процессы.\nФинансовая сфера постоянно развивается, особенно с учетом внедрения новых технологий. Это дает студентам возможность работать в динамичной и перспективной области.\nОбучение по этому направлению позволяет приобрести специальные навыки в области финансового менеджмента, а также финансовых технологий, включая блокчейн, искусственный интеллект и цифровые платежи.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 250\nВечернее: 100\nЗаочное: 1000\n\nРусский\nОчное: 100\nВечернее: 50\nЗаочное: 150",
        "Требования к поступлению": "Математика – 3,1 балла\n(25 вопросов)\n\nАнглийский язык – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Банковское дело и аудит": {
        "image": "http://telegra.ph//file/562a1ee48a607eb111210.jpg",
        "Информация о направлении": "'Банковское дело и аудит' дает студентам глубокие знания в области банковского дела, финансового аудита и управления рисками. В процессе обучения студенты изучают принципы работы банков, методы финансового аудита, а также осваивают принципы оценки и управления финансовыми рисками.\nВыпускники, специализирующиеся в области 'Банковское дело и аудит', могут продолжить работу в банковском секторе, стать финансовыми аудиторами, менеджерами по рискам или специалистами по корпоративным финансам. Они также могут выбрать карьеру в консалтинге, управлении капиталом, финансовых отделах компаний или в области аудита и консалтинга.\nПочему стоит выбрать направление 'Банковское дело и аудит'? Банковский сектор постоянно растет и развивается, создавая новые рабочие места и возможности. Современные технологии и изменения в финансовой сфере делают это направление особенно востребованным. Квалифицированные специалисты в области банковского дела и аудита помогают обеспечивать финансовую стабильность и снижать риски в период экономической неопределенности. Эти специалисты востребованы как на национальном, так и на международном уровне.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 200\nВечернее: 100\nЗаочное: 1000\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 100",
        "Требования к поступлению": "Математика – 3,1 балла\n(25 вопросов)\n\nАнглийский язык – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Программная инженерия": {
        "image": "http://telegra.ph//file/91e10743020695f5cf596.jpg",
        "Информация о направлении": "'Программная инженерия' дает студентам глубокие знания в области разработки программного обеспечения, архитектуры компьютерных систем и методологии программирования. В процессе обучения студенты осваивают различные языки программирования, анализируют алгоритмы и изучают современные технологии разработки.\nВыпускники направления 'Программная инженерия' могут начать работу в области информационных технологий в качестве разработчиков, инженеров программного обеспечения, системных аналитиков или тестировщиков. Они также могут выбрать карьеру в научных исследованиях, инновационных разработках программных продуктов. Кроме того, выпускники могут работать в технологических стартапах, компаниях по разработке приложений, а также в компаниях, занимающихся искусственным интеллектом и машинным обучением.\nСпрос на квалифицированных разработчиков стремительно растет в условиях цифровой трансформации и увеличения значимости информационных технологий. Современные технологии, такие как искусственный интеллект, машинное обучение и большие данные, требуют специалистов, способных разрабатывать и обслуживать сложные программные решения. Программная инженерия предоставляет необходимые знания и навыки для работы в передовых областях, что делает ее очень актуальной и перспективной сферой.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 150\nВечернее: 100\nЗаочное: 150\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 50",
        "Требования к поступлению": "Математика – 3,1 балла\n(25 вопросов)\n\nАнглийский язык – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    },
    "Туризм": {
        "image": "http://telegra.ph//file/c9b1988cffa2a4a2547e1.jpg",
        "Информация о направлении": "'Туризм' дает студентам глубокие знания в области организации и управления туристическими услугами, а также национального и международного туризма. В процессе обучения студенты изучают основы гостеприимства, маркетинг туризма и различные аспекты управления туристическим бизнесом.\nВыпускники направления 'Туризм' могут найти работу в гостиничном бизнесе, у туроператоров, в агентствах по организации мероприятий и даже в культурных учреждениях, связанных с туризмом. Они могут стать менеджерами по туризму, экскурсоводами, специалистами по разработке туристических маршрутов или заниматься международным туризмом. Кроме того, выпускники могут выбрать карьеру в консалтинге по туризму, управлении мероприятиями или начать собственное предпринимательство в сфере туризма.\nСовременный туризм активно развивается благодаря глобализации, росту международных путешествий и увеличению количества туристических направлений. Туристическая индустрия восстанавливается после пандемии и предлагает уникальные возможности для специалистов, способных внедрять инновационные решения и предоставлять высококачественные услуги. Туризм способствует экономическому развитию регионов, укреплению культурных связей и повышению качества жизни, что делает его актуальным и перспективным направлением.",
        "Квота на 2024/2025 год": "Узбекский\nОчное: 150\nВечернее: 100\nЗаочное: 400\n\nРусский\nОчное: 50\nВечернее: 50\nЗаочное: 100",
        "Требования к поступлению": "История – 3,1 балла\n(25 вопросов)\n\nАнглийский язык – 2,1 балла\n(25 вопросов)\n\nЛогические вопросы – 1,1 балла\n(10 вопросов)"
    }
}


CONTRACT_INFO_UZ = {
    "Logistika": {
        "Kunduzgi": "4 yil – 16 800 000 so’m",
        "Kechki": "4,5 yil – 12 600 000 so’m",
        "Sirtqi": "5 yil – 12 900 000 so’m"
    },
    "Maktabgacha ta’lim": {
        "Kunduzgi": "3 yil – 12 900 000 so’m",
        "Kechki": "3,5 yil – 7 900 000 so’m",
        "Sirtqi": "4 yil – 12 600 000 so’m"
    },
    "Boshlang’ich ta’lim": {
        "Kunduzgi": "4 yil – 16 800 000 so’m",
        "Kechki": "4,5 yil – 12 600 000 so’m",
        "Sirtqi": "5 yil – 12 600 000 so’m"
    },
    "Tarix": {
        "Kunduzgi": "4 yil – 16 800 000 so’m",
        "Kechki": "4,5 yil – 7 900 000 so’m",
        "Sirtqi": "5 yil – 12 900 000 so’m"
    },
    "Xorijiy til va adabiyoti": {
        "Kunduzgi": "4 yil – 16 800 000 so’m",
        "Kechki": "4,5 yil – 12 600 000 so’m"
    },
    "Iqtisodiyot": {
        "Kunduzgi": "4 yil – 19 800 000 so’m",
        "Kechki": "4,5 yil – 14 500 000 so’m",
        "Sirtqi": "5 yil – 14 850 000 so’m"
    },
    "Psixologiya": {
        "Kunduzgi": "4 yil – 16 800 000 so’m",
        "Kechki": "4,5 yil – 12 600 000 so’m",
        "Sirtqi": "5 yil – 12 900 000 so’m"
    },
    "Buxgalteriya hisobi": {
        "Kunduzgi": "4 yil – 19 800 000 so’m",
        "Kechki": "4,5 yil – 14 500 000 so’m",
        "Sirtqi": "5 yil – 14 850 000 so’m"
    },
    "Moliya va moliyaviy texnologiyalar": {
        "Kunduzgi": "4 yil – 19 800 000 so’m",
        "Kechki": "4,5 yil – 14 500 000 so’m",
        "Sirtqi": "5 yil – 14 850 000 so’m"
    },
    "Bank ishi": {
        "Kunduzgi": "4 yil – 19 800 000 so’m",
        "Kechki": "4,5 yil – 14 500 000 so’m",
        "Sirtqi": "5 yil – 14 850 000 so’m"
    },
    "Dasturiy injiniring": {
        "Kunduzgi": "4 yil – 16 800 000 so’m",
        "Kechki": "4,5 yil – 8 800 000 so’m",
        "Sirtqi": "5 yil – 12 900 000 so’m"
    },
    "Turizm va mehmondoʻstlik": {
        "Kunduzgi": "4 yil – 16 800 000 so’m",
        "Kechki": "4,5 yil – 8 800 000 so’m",
        "Sirtqi": "5 yil – 12 600 000 so’m"
    }
}

CONTRACT_INFO_RU = {
    "Логистика": {
        "Очная": "4 года – 16 800 000 сум",
        "Вечерняя": "4,5 года – 12 600 000 сум",
        "Заочная": "5 лет – 12 900 000 сум"
    },
    "Дошкольное образование": {
        "Очная": "3 года – 12 900 000 сум",
        "Вечерняя": "3,5 года – 7 900 000 сум",
        "Заочная": "4 года – 12 600 000 сум"
    },
    "Начальное образование": {
        "Очная": "4 года – 16 800 000 сум",
        "Вечерняя": "4,5 года – 12 600 000 сум",
        "Заочная": "5 лет – 12 600 000 сум"
    },
    "История": {
        "Очная": "4 года – 16 800 000 сум",
        "Вечерняя": "4,5 года – 7 900 000 сум",
        "Заочная": "5 лет – 12 900 000 сум"
    },
    "Иностранный язык и литература": {
        "Очная": "4 года – 16 800 000 сум",
        "Вечерняя": "4,5 года – 12 600 000 сум"
    },
    "Экономика": {
        "Очная": "4 года – 19 800 000 сум",
        "Вечерняя": "4,5 года – 14 500 000 сум",
        "Заочная": "5 лет – 14 850 000 сум"
    },
    "Психология": {
        "Очная": "4 года – 16 800 000 сум",
        "Вечерняя": "4,5 года – 12 600 000 сум",
        "Заочная": "5 лет – 12 900 000 сум"
    },
    "Бухгалтерский учет": {
        "Очная": "4 года – 19 800 000 сум",
        "Вечерняя": "4,5 года – 14 500 000 сум",
        "Заочная": "5 лет – 14 850 000 сум"
    },
    "Финансы и финансовые технологии": {
        "Очная": "4 года – 19 800 000 сум",
        "Вечерняя": "4,5 года – 14 500 000 сум",
        "Заочная": "5 лет – 14 850 000 сум"
    },
    "Банковское дело": {
        "Очная": "4 года – 19 800 000 сум",
        "Вечерняя": "4,5 года – 14 500 000 сум",
        "Заочная": "5 лет – 14 850 000 сум"
    },
    "Программная инженерия": {
        "Очная": "4 года – 16 800 000 сум",
        "Вечерняя": "4,5 года – 8 800 000 сум",
        "Заочная": "5 лет – 12 900 000 сум"
    },
    "Туризм": {
        "Очная": "4 года – 16 800 000 сум",
        "Вечерняя": "4,5 года – 8 800 000 сум",
        "Заочная": "5 лет – 12 600 000 сум"
    }
}
