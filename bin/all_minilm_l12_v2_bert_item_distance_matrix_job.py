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
        host      = 'http://localhost:8000',
        temp_path = '/home/adrian/development/personal/maestria/rec-sys/temp'
    ).bert_item_distance_matrix_job('all-MiniLM-L12-v2').execute()