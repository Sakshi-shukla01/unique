{ pkgs }: {
  deps = [
    pkgs.python311Full
    pkgs.gunicorn
    pkgs.pip
  ];
}
