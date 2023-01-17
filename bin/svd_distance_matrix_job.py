#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import sys
sys.path.append('./src')
from domain_context import DomainContext
#------------------------------------------------------------------------------
#
#
#
#
#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
if __name__ == '__main__':
    DomainContext(
        host      = 'http://recsys.sytes.net',
        temp_path = '/home/adrian/development/personal/maestria/rec-sys/temp'
    ).svd_distance_matrix_job.execute()
