{pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs.python311Packages; 
  [pandas 
   pipx
   evdev
    ];
}

