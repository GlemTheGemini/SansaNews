import instaloader
#archivo_users = open("users.txt")
L = instaloader.Instaloader(download_pictures=False, compress_json=False, download_videos=False,post_metadata_txt_pattern="")
perfil = "dead.vibes.x"
L.download_profile(perfil,fast_update=True)
