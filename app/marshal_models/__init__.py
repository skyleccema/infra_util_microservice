from .api_marshalling import *
from .generic_models import (DictGenericModel, ListGenericModel,
                            TupleGenericModel, im,
                            IntGenericModel, StrGenericModel, GenericGetStbStatusBroken)
from .get_stb_status_broken_model import GetStbStatusBrokenOut, GetStbStatusBrokenDTOOut
from .available_slots_model import AvailableSlotsOut, AvailableSlotsDTOOut
from .get_ip_model import GetIpOut, GetIpDTOOut
# from .query_stb_info_model import QueryStbInfoIn, QueryStbInfoModel
from .query_stb_info_model import QueryStbInfoOut, QueryStbInfoDTO
from .get_all_stb_model import GetAllStbDTOOut, GetAllStbOut
from .fetch_rack_slot_type_by_project_model import FetchRackSlotTypeByProjectOut, FetchRackSlotTypeByProjectDTO
