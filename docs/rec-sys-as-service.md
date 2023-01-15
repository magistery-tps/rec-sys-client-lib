## Correr [RecSys](http://recsys.sytes.net:8000) como servicio [systemd](https://systemd.io/)


**Step 1**: Clonar repo.

```bash
$ cd ~
$ git clone https://github.com/magistery-tps/rec-sys.git
$ mv airflow-systemd airflow
$ cd recsys
```

**Step 2**: Crear conda environment requerido para correr recsys como un servicio.

```bash
$ conda env update -f environment.yml
```

**Step 3**: Copiar file.service a `~/.config/systemd/user/`:

```bash
$ cp recsys.service ~/.config/systemd/user/
```

**Step 4**: Importar variable de entoeno requeridas por la aplicación:

```bash
$ echo "source ~/rec-sys/.shell.recsysrc" >> ~/.bashrc
ó
$ echo "source ~/rec-sys/.shell.recsysrc" >> ~/.zshrc
```


**Step 4**: Referscar la configuración de systemd.

```bash
$ systemctl --user daemon-reload
```

**Step 5**: Habilitar el servicio apra que se inie al bootear el sistema.

```bash
$ systemctl --user enable recsys
```

**Step 6**: Iniciar el servicio en background.

```bash
$ systemctl --user start recsys
```
