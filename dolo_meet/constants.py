from toolkit.fileutils import Fileutils
from toolkit.logger import Logger

SDIR = "../../"
FUTL = Fileutils()
CRED = FUTL.get_lst_fm_yml(SDIR + "dolo-meet.yml")
CSVF = SDIR + "nse_fo.csv"
logging = Logger(10)
