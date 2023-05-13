#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------
import sys
sys.path.append('./src')
from domain_context import DomainContext
from pathlib import Path
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
        host      = 'http://nonosoft.ddns.net:8000',
        temp_path = f'{Path.home()}/rec-sys/temp'
    ).bert_item_distance_matrix_job('all-MiniLM-L12-v2').execute()
