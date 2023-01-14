# Isntall in Google Cloud

## Steps


**Step 1**: Create a micro 2 cores and 3 GB of ram VM.
**Step 2**: SSD Disck 10GB.
**Step 3**: Ubuntu 18 LTS.
**Step 4**: Access vya SSH shell.
**Step 5**: Enable swap memory.

    ```bash
    $ sudo fallocate -l 1G /swapfile
    $ sudo chmod 600 /swapfile
    $ sudo mkswap /swapfile
    $ sudo swapon /swapfile
    $ sudo cp /etc/fstab /etc/fstab.bak
    $ echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    ```

**Step 6**: Install mariadb.

    ```bash
    $ sudo apt update
    $ sudo apt-get install software-properties-common
    $ sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
    $ sudo add-apt-repository 'deb [arch=amd64] http://mirror.zol.co.zw/mariadb/repo/10.3/ubuntu bionic main'
    $ sudo apt update
    $ sudo apt install mariadb-server
    ```

**Step 7**: Install miniconda.

    ```bash
    $ curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh
    $ chmod +x Miniconda3-latest-Linux-x86_64.sh
    $ bash Miniconda3-latest-Linux-x86_64.sh
    $ source ~/.bashrc
    ```

**Step 9**: Install default dev tools used to compile packages.

    ```bash
    $ sudo apt-get install build-essential gcc make perl dkms
    ```

**Step 10**: Install mamba.

    ```bash
    $ conda install -c conda-forge mamba
    ```

**Step 11**: Clone rec-sys repository.

```bash
$ git clone https://github.com/magistery-tps/rec-sys.git
$ cd rec-sys
```

**Step 12**: Crear environment.

```bash
$ mamba env create -f environment.yml
```

**Step 13**: Activar environment.

```bash
$ conda activate rec-sys
```

**Step 14**: Asign a passworf to root database user.

```bash
$ sudo mysqladmin -u root password
```

**Step 15**: Create database.

```bash
$ mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS recsys"
```

**Step 15**: import database dump.

```bash
$ mysqldump -u root -p
```

```sql
MariaDB [recsys]> Use recsys;
Database changed
```

```sql
MariaDB [recsys]> source /home/adrianmarino1000/rec-sys/database/recsys_database.sql
```

```sql
MariaDB [recsys]> show tables;
+-----------------------------------------------+
| Tables_in_recsys                              |
+-----------------------------------------------+
| account_emailconfirmation                     |
| auth_group                                    |
...
| taggit_tag                                    |
| taggit_taggeditem                             |
+-----------------------------------------------+
31 rows in set (0.00 sec)
```

```sql
MariaDB [recsys]> exit;
```

**Step 16**: Copiar file.service a `~/.config/systemd/user/`:

```bash
$ mkdir -p ~/.config/systemd/user
$ cp -v recsys.service ~/.config/systemd/user/
```

**Step 17**: Importar variable de entoeno requeridas por la aplicación:

```bash
$ echo "source ~/rec-sys/.shell.recsysrc" >> ~/.bashrc
```

**Step 18**: Referscar la configuración de systemd.

```bash
$ systemctl --user daemon-reload
```

**Step 19**: Habilitar el servicio apra que se inie al bootear el sistema.

```bash
$ systemctl --user enable recsys
```

**Step 20**: Config our database root password.

```bash
$ vim rec-sys/recsys/settings.py
```

```python
DATABASES = {
    'default': {
        ...
        'PASSWORD': 'MY_PASSWORD',
        ...
    }
}
```

**Step 21**: Config isntalled miniconda path adn server port.

```bash
$ vim service.conf
```

```python
export CONDA_PATH="$HOME/miniconda3"
export PORT="80"
```

**Step 21**: Start rec-sys app service.

```bash
$ systemctl --user start recsys
```
