# Domain
from ..models  import SimilarityMatrixCell
from ..logger  import get_logger
from collections import OrderedDict


class SimilarityMatrixService:
    def __init__(self):
        self.logger = get_logger(self)

    def find_similar_element_ids(self, matrix, element_id, limit):
        similar_col_cells = SimilarityMatrixCell.objects.filter(
            row       = element_id,
            matrix    = matrix.id,
            version   = matrix.version,
            value__gt = 0
        )

        sim_by_id = { cell.column: cell.value for cell in similar_col_cells }

        similar_row_cels = SimilarityMatrixCell.objects.filter(
            column  = element_id,
            matrix  = matrix.id,
            version = matrix.version,
            value__gt = 0
        )

        for cell in similar_row_cels:
            if cell.row in sim_by_id:
                if cell.value >= sim_by_id[cell.row]:
                    sim_by_id[cell.row] = cell.value
            else:
                sim_by_id[cell.row] = cell.value


        id_sim_list = list(sim_by_id.items())
        id_sim_list.sort(key=lambda id_sim: id_sim[1], reverse=True)
        id_sim_list = id_sim_list[:limit]

        orderd_dict = OrderedDict()
        for id_sim in id_sim_list:
            if id_sim[0] != element_id:
                orderd_dict[id_sim[0]] = id_sim[1]

        return orderd_dict