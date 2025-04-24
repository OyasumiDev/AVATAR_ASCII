# main.py
import tkinter as tk
from tkinter import filedialog
from app.ASCCI.IMAGEN.ascii_image import image_to_ascii,ascii_to_image
from app.ASCCI.VIDEO.ascii_video import video_to_ascii

def main():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.lift()
    root.update()

    while True:
        print("\n=== ASCII Converter ===")
        print("1) Convertir imagen a ASCII")
        print("2) Convertir video a ASCII")
        print("3) Salir")
        choice = input("Selecciona [1/2/3]: ").strip()

        if choice == '1':
            img = filedialog.askopenfilename(parent=root,
                title="Selecciona imagen",
                filetypes=[("Imágenes","*.png *.jpg *.jpeg *.bmp *.gif"),("Todos","*.*")])
            if not img:
                print("No seleccionaste ninguna imagen."); continue
            print("Formato de salida:\n1) Texto (.txt)\n2) Imagen (.png)")
            fmt = input("Selecciona [1/2]: ").strip()
            if fmt == '1':
                out = filedialog.asksaveasfilename(parent=root,
                    title="Guardar como texto", defaultextension=".txt",
                    filetypes=[("Texto","*.txt"),("Todos","*.*")])
                if out:
                    art = image_to_ascii(img)
                    with open(out,'w',encoding='utf-8') as f: f.write(art)
                    print(f"Guardado en: {out}")
            elif fmt == '2':
                out = filedialog.asksaveasfilename(parent=root,
                    title="Guardar como imagen", defaultextension=".png",
                    filetypes=[("PNG","*.png"),("Todos","*.*")])
                if out:
                    art = image_to_ascii(img)
                    img_out = ascii_to_image(art)
                    img_out.save(out)
                    print(f"Imagen guardada en: {out}")
            else:
                print("Formato inválido.")

        elif choice == '2':
            vid = filedialog.askopenfilename(parent=root,
                title="Selecciona video",
                filetypes=[("Videos","*.mp4 *.avi *.mov *.mkv *.flv"),("Todos","*.*")])
            if not vid:
                print("No seleccionaste ningún video."); continue
            print("Formato de salida:\n1) Texto (frames .txt)\n2) Imagen (frames .png)\n3) Video (.mp4)")
            fmt = input("Selecciona [1/2/3]: ").strip()
            if fmt in ('1','2'):
                out_dir = filedialog.askdirectory(parent=root,
                    title="Selecciona carpeta de salida")
                if out_dir:
                    fmt_str = 'text' if fmt=='1' else 'image'
                    video_to_ascii(vid, out_dir, output_format=fmt_str)
            elif fmt == '3':
                out = filedialog.asksaveasfilename(parent=root,
                    title="Guardar como video", defaultextension=".mp4",
                    filetypes=[("MP4","*.mp4")])
                if out:
                    video_to_ascii(vid, out, output_format='mp4')
            else:
                print("Formato inválido.")

        elif choice == '3':
            print("Saliendo..."); break
        else:
            print("Opción inválida.")

if __name__ == '__main__':
    main()
