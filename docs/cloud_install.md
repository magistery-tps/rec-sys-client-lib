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
**Step 6**: Update pacakge index.

    ```bash
    $ sudo apt update
    ```

**Step 7**: Install maridb:

    ```bash
    $ sudo install mariadb-server
    ```

**Step 8**: Install mariadb.

    ```bash
    $ sudo install mariadb-server
    ```

**Step 9**: Install miniconda.

    ```bash
    $ curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh
    $ chmod +a Miniconda3-latest-Linux-x86_64.sh
    $ bash Miniconda3-latest-Linux-x86_64.sh
    $ source ~/.bashrc
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
$ mamba activate rec-sys
```

**Step 14**: Create database.

```bash
$ mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS recsys"
```

**Step 15**: import database dump.

```bash
$ mysqldump -u root -p  recsys <> database/recsys_database.sql
```

**Step 16**: Copiar file.service a `~/.config/systemd/user/`:

```bash
$ cp recsys.service ~/.config/systemd/user/
```

**Step 17**: Importar variable de entoeno requeridas por la aplicación:

```bash
$ echo "source ~/recsys/.shell.recsysrc" >> ~/.bashrc
```

**Step 18**: Referscar la configuración de systemd.

```bash
$ systemctl --user daemon-reload
```

**Step 19**: Habilitar el servicio apra que se inie al bootear el sistema.

```bash
$ systemctl --user enable recsys
```

**Step 20**: Iniciar el servicio en background.

```bash
$ systemctl --user start recsys
```