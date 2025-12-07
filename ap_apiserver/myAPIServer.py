#############################################
#
# Just a whole bunch of useful apis
# Change
#############################################

import hmac, os
from flask import Flask,jsonify, make_response, request, Blueprint, jsonify, current_app
from git import Repo

app = Flask(__name__)
webhook = Blueprint('webhook', __name__, url_prefix='')
app.config['BITBUCKET_SECRET'] = os.environ.get('GITHUB_SECRET')
app.config['REPO_PATH'] = os.environ.get('REPO_PATH')
app.register_blueprint(webhook)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/hello/<myname>')
def hello_name(myname):
    return 'Hello %s!' % myname

@app.route('/json')
def deliver_json():
    return jsonify(
      id='chopstick_id',
      color='bamboo',
      left_handed=True,
    )

@app.route('/pullapsa', methods=['POST'])
def handle_bitbucket_hook():
# """ Entry point for bitbucket webhook """
#  signature = request.headers.get('X-Hub-Signature')
#  if signature is not None:
#    sha, signature = signature.split('=')
#  secret = str.encode('asecretpassphraseusebygithubwebhook')
#  hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
#  if hmac.compare_digest(hashhex, signature):
  repo = Repo('/home/mantri/APSA')
  origin = repo.remotes.origin
  origin.pull('--force')
  #commit = request.json['after'][0:6]
  commit = request.json
  print('Repository updated with commit {}'.format(commit))
  return jsonify({}), 200

@app.route('/json1')
def deliver_json1():
    return jsonify(
      [
    {
        "id": 1364,
        "user_id": 2702,
        "title": "At aestus sordeo speculum curtus minima.",
        "body": "Caveo adsuesco admitto. Tandem commodo curo. Cursus arbor celer. Caveo theatrum cubitum. Crepusculum victoria una. Aqua minima coepi. Ancilla aut blanditiis. Apud cerno repellat. Carmen voco vae. Arca volup illum. Antiquus correptius est. Correptius quisquam beatus. Ullus terror consequatur. Conturbo vallum crudelis. Canto dolorem amplitudo. Talus succurro nobis. Censura validus antepono. Armarium tribuo cognomen. Concido eum spargo. Caterva aveho aufero. Debilito repellendus sufficio."
    },
    {
        "id": 1362,
        "user_id": 2698,
        "title": "Confero addo benevolentia agnosco tracto tepidus consequatur suspendo ad aegrus celer voluptatum decens.",
        "body": "Conforto coma derelinquo. Theologus curriculum volutabrum. Centum fuga despirmatio. Neque corroboro rerum. Umerus voluptas patior. Carcer adsum odit. Adstringo dedecor adeptio. Adeptio vivo torrens. Deinde itaque cultellus. Conculco xiphias convoco. A et officiis. Certo admoneo rerum. Decipio tribuo unus. Textus porro appono. Ambulo contego colloco."
    },
    {
        "id": 1361,
        "user_id": 2698,
        "title": "Comparo confido placeat corpus caecus enim et tui denique bonus tricesimus sed eveniet animi conqueror cum amaritudo aqua.",
        "body": "Abutor conventus clibanus. Vinculum thymbra creber. Quasi cohibeo commodo. Defetiscor subito veritas. Turpis exercitationem aureus. Contra cum necessitatibus. Temptatio canis tam. Decens atrocitas conitor. Attollo theca beatae. Sponte tamquam ustulo. Vita demitto ultio. Creta adeo alii. Reiciendis clamo amicitia. Sonitus aut stips. Stultus ut deinde. Strues vociferor sumo. Ad voluptatem minus. Numquam contra molestiae."
    },
    {
        "id": 1360,
        "user_id": 2695,
        "title": "Tolero temeritas confero speciosus teneo pauci quia.",
        "body": "Clamo peior occaecati. Color contabesco voluptas. Comparo acervus volva. Cedo conatus ulciscor. Sunt aer confero. Depereo conicio suffoco. Et defero alveus. Aduro subseco itaque. Tergeo magni quia. Curiositas ascisco accipio. Coma colligo cura. Velut tenetur ullus. Candidus volubilis solutio. Condico velociter ter. Ipsam vapulus cui. Tot delego tendo."
    },
    {
        "id": 1359,
        "user_id": 2689,
        "title": "Deprimo ventito triduana tendo carus paulatim certo condico titulus depraedor denuo eos laborum conicio est templum utor quidem.",
        "body": "Comburo casso ut. Capitulus et valens. Bos adulatio cena. Tui tamdiu rem. Abscido adsum officiis. Sono saepe pauper. Curriculum votum claustrum. Speciosus audeo colloco. Despirmatio ab triumphus. Acer tempore uter. Spectaculum delego cattus. Acervus voluptas a. Aut adfero exercitationem. Dedecor careo cur. Brevis doloribus voluptatibus. Tubineus complectus degusto. Voveo comedo voluptatum. Tempus architecto arbitro. Theca velut arcus."
    },
    {
        "id": 1358,
        "user_id": 2686,
        "title": "Crux saepe acervus depraedor vulgus ocer qui tamquam timor suffoco amoveo conculco utique demonstro dolores.",
        "body": "Curiositas tabella claustrum. Vespillo concido pauper. Vigor verbera ad. Desolo argentum calculus. Cur amplitudo varietas. Tenus facilis coma. Beatus absque in. Molestias vulgus dolor. Laborum taceo beatus. Cresco uxor voro. Vetus aestas depono. Arceo succedo spiritus. Eligendi amplitudo vel. Vomito creo pecto. Cibo absque brevis. Mollitia bestia speculum. Speculum desolo subiungo."
    },
    {
        "id": 1357,
        "user_id": 2686,
        "title": "Voluptatem suscipio maiores aurum vulgaris iste quia capio cupio atrox.",
        "body": "Vinum aliquam alienus. Tepesco aut tracto. Cognatus aegrotatio coadunatio. Talus excepturi verbum. Atque collum arbor. Adfero ad amiculum. Alienus defessus stabilis. Curiositas suffoco stabilis. Delibero vulgivagus varius. Dolores tutis cras. Spargo demulceo auditor. Viduo verus supplanto. Ventus autus volutabrum. Repudiandae argentum ullam. Cito natus texo. Sumo vapulus placeat. Contego damnatio alveus. Nobis aqua coniecto. Validus cuppedia ter."
    },
    {
        "id": 1356,
        "user_id": 2685,
        "title": "Accipio voro stultus cupiditate verto valde colo demonstro cogito ocer aperte defungo ventito qui ademptio auctor coruscus adfero tero.",
        "body": "Vilitas nisi caute. Adulescens spargo defessus. Despecto quo callide. Adopto cupiditas corporis. Apostolus totus arguo. Umquam tolero voluptates. Voluptates amissio cornu. Terreo coadunatio advoco. Sto nulla utilis. Dolor umquam defleo. Cruentus creo dolorem. Odio arceo doloremque. Pecus soluta ocer. Adultus ut terga. Valde acer admitto. Armo conitor verus. Auditor vorago vito. Nam depromo canis. Vallum non sit. Astrum derelinquo supra. Soleo depromo votum."
    },
    {
        "id": 1355,
        "user_id": 2685,
        "title": "Cohors qui considero vel sit versus sit careo quia titulus capto.",
        "body": "Cito enim et. Voco dolore celer. Clamo venia voluptas. Clam deficio est. Adsuesco et desino. Subiungo timidus neque. Totus et thorax. Concedo illo urbanus. Cum decet aperiam. Timidus sufficio beatae. Soleo alienus arcesso. Adaugeo incidunt adultus. Vilitas expedita vinculum. Aspernatur qui numquam. Est quo acies. Vomica approbo alter. Aetas brevis pax. Demum adhuc impedit. Ut talus sit. Similique verbera tersus. Demergo quia defessus."
    },
    {
        "id": 1354,
        "user_id": 2681,
        "title": "Adflicto speciosus socius vel excepturi talio arto soleo cogo impedit conspergo damno.",
        "body": "Rerum deinde dolorum. Adversus eligendi tres. Quis cur vitiosus. Conduco bonus nulla. Comminor tantillus artificiose. Tempora vinculum alii. Tristis ea beneficium. Voveo aut decens. Tego sol trepide. Certus pel sum. Aliqua abstergo speculum. Una appono textor. Venia porro vomer. Textilis benevolentia sum. Venia comminor enim."
    },
    {
        "id": 1353,
        "user_id": 2681,
        "title": "Explicabo absum tumultus certe sulum utilis baiulus veritas.",
        "body": "Cognatus chirographum accipio. Ducimus in tamisium. Vilicus speciosus aut. Demens suffoco conforto. Vitae quo aut. Terror aequus qui. Acer caecus vero. Vito voluptates dolore. Caries sit aestas. Conor bestia tametsi. Verus arbitro suppellex. Timidus dolorem calculus. Unde molestiae recusandae. Sustineo angulus textus. Vulticulus verumtamen bonus. Speculum defetiscor damno."
    },
    {
        "id": 1352,
        "user_id": 2674,
        "title": "Undique universe aggredior vallum tero defetiscor quam suppellex creator cupressus qui.",
        "body": "Admoveo voluptas utor. Admoneo sol adipiscor. Termes solus basium. Curatio desipio quo. Attero adipiscor sonitus. Adnuo doloribus comptus. Tumultus paens aegre. Calcar veritatis absorbeo. Corpus amiculum abundans. Clementia advoco paens. Taceo thymbra super. Ipsam et animi. Tabesco curis artificiose. Cilicium auctus admitto. Amplitudo apto sulum. Repellat compello succurro."
    },
    {
        "id": 1351,
        "user_id": 2673,
        "title": "Bonus civis vero amplexus ascisco tener incidunt consequatur creo acidus xiphias averto cetera aequitas surgo terreo abstergo admiratio tenus.",
        "body": "Clarus optio qui. Animi deorsum allatus. Annus credo aureus. Concedo qui adfero. Solutio sollers decor. Quam acervus odio. Officiis turbo aufero. Asperiores dolores vultuosus. Damno sint voveo. Amitto bardus arto. Quia approbo spoliatio. Adamo absconditus testimonium. Acsi chirographum quam. Tamquam centum corrupti. Ut tantum tergiversatio. Creber aveho tabella. Creo sodalitas colloco. Congregatio averto desolo. Volup admitto curo."
    },
    {
        "id": 1350,
        "user_id": 2673,
        "title": "Cur vitae velit dolores vorago contego incidunt velum varietas dolor capio strues.",
        "body": "Vox caste dolor. Velit aut sapiente. Sono umerus conitor. Supellex studio viscus. Adfectus beneficium acidus. Carpo victus tepesco. Acceptus libero defero. Nostrum amplexus minus. Illo nisi vero. Desino degenero crur. Nihil auxilium fuga. Dapifer virtus annus. Torqueo alioqui delectus. Vel spes comedo. Ullam non volaticus. Cibo iusto utrum."
    },
    {
        "id": 1349,
        "user_id": 2672,
        "title": "Vilis id omnis annus vulnero arcus pariatur corrigo et condico nobis carcer concedo censura denuncio aveho caste eveniet.",
        "body": "Textor sunt verecundia. Alveus contego ustulo. Vel aspernatur crapula. Tamquam cum coepi. Quod ut acerbitas. Tibi maiores et. Asper tener aqua. Vitium et utroque. Creta utique assentator. Sint itaque virtus. Succedo voluptatem tonsor. Sit alii virgo. Crastinus tergiversatio tabernus. Arguo voluptatem capitulus. Abutor tracto vitiosus. Ut alienus aspernatur. Adfectus cras cui. Currus corpus admoneo. Somnus aliqua adsidue."
    },
    {
        "id": 1348,
        "user_id": 2670,
        "title": "Sordeo triumphus tepidus antiquus abduco desino decet ab ait.",
        "body": "Autem corona cibus. Altus tunc quibusdam. Amitto cuius aqua. Cultura ut adhuc. Altus adaugeo adeptio. Amitto sed rem. Est color calcar. Undique inflammatio ipsum. Vulticulus umerus conscendo. Barba voluptates curis. Caries thermae eos. Cupiditate adulatio contabesco. Quod armarium possimus. Cruentus vespillo considero. At caute auxilium. Appello demonstro suadeo. Volup tametsi careo."
    },
    {
        "id": 1347,
        "user_id": 2669,
        "title": "Accipio sunt ascisco attollo conservo cariosus defigo vomica celo adversus vinco caute corroboro sit necessitatibus terminatio unus molestiae.",
        "body": "Inflammatio vicinus omnis. Minima desipio apud. Adhaero terror turbo. Subvenio coepi odio. Iure vel vomica. Terga texo aliqua. Universe thema concedo. Unde caecus cursim. Callide auditor varius. Tactus coruscus cubicularis. Conitor colligo perspiciatis. Maiores ara creber. Tricesimus defessus infit. Calamitas cum voluptatum. Vulpes aperio thorax. Aranea terga vestigium. Caecus aveho uter. Tego cras venio."
    },
    {
        "id": 1346,
        "user_id": 2668,
        "title": "Versus sum acer coepi laudantium tardus exercitationem soleo summopere.",
        "body": "Tamisium rerum depulso. Fugit adultus aiunt. Crastinus eligendi tristis. Quis cilicium demulceo. Caelestis demergo deripio. Tener voluptatem vulgus. Admoveo abundans decimus. Tardus victoria celebrer. Delectus tenetur tabesco. Qui adsum concedo. Abundans sumo admoveo. Sui contabesco civis. Sed confido addo. Suppono celebrer solitudo. Defero vigor itaque. Damno armarium paens."
    },
    {
        "id": 1345,
        "user_id": 2666,
        "title": "Correptius ventus velociter vomer theca dedecor admoveo abutor vindico suspendo deleo perferendis.",
        "body": "Cena cui vulnus. Demonstro sunt suscipio. Victus tabesco defungo. Volva volubilis voluptas. Caelestis valens virga. Adiuvo error ullus. Cohibeo volutabrum creber. Quas timidus calcar. Tristis cupiditate omnis. Triduana quam venia. Inventore decretum demulceo. Cibus spiritus minima. Qui vetus suggero. Virga acquiro velum. Tendo vir venustas. Eos magnam deduco. Assentator peccatus adulescens."
    },
    {
        "id": 1344,
        "user_id": 2666,
        "title": "Asperiores coepi est aut ea deorsum sed ut anser vapulus et nam studio et caelestis cuius alii voluptatem.",
        "body": "Suppellex aspicio voveo. Totus crastinus contego. Corrumpo vix agnitio. Amita vesper cado. Dolorem tumultus suadeo. Tyrannus summa audio. Aperte adflicto commemoro. Demoror comburo ambitus. Abscido voro cupiditas. Voluptatem in rerum. Recusandae viduata cohors. Consequatur neque thalassinus. Cupiditas alveus accommodo. Vesica nihil artificiose. Solum expedita dicta. Caute vespillo supellex. Altus colo velut. Vergo solium thymbra. Civitas vespillo nam. Stips depromo turpe. Depromo venio angelus."
    }
]
)
