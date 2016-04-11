from .app import manager, db

@manager.command
def loaddb(filename):
    '''Creates the tables and populates them with data.'''

    #creation de toutes les tables
    db.create_all()

    #chargement de notre jeu de données
    import yaml
    albums = yaml.load(open(filename))

    #import des modèles
    from .models import Artist, Album, Genre, get_genre

    #creation de tous les auteurs
    dict_artists = {}
    dict_genres={}
    for b in albums:
        a = b["by"]
        #si l'artiste n'est pas encore dans la table Artist il faut l'y ajouter
        if a not in dict_artists:
            o = Artist(name=a)
            dict_artists[a]=o
            #on ajoute l'artiste créé à la db
            db.session.add(o)
            #il faut commit ici pour qu'on puisse récupérer le champ id de l'instance d'Artist lors de la création de l'album ci dessous
            db.session.commit()
        album = Album(id            = b["entryId"],
                      title         = b["title"],
                      releaseYear   = b["releaseYear"],
                      img           = b["img"],
                      compositor    = b["parent"],
                      artist_id     = dict_artists[a].id,
        )
        liste_genre = b["genre"]
        for g in liste_genre:
            #si le genre n'est pas encore dans la table genre il faut l'y ajouter
            if g not in dict_genres:
                o = Genre(name_g=g)
                dict_genres[g]=o
                #on ajoute le genre créé à la db
                db.session.add(o)
            #on ajoute à l'abum le genre qui lui correspond
            genre = dict_genres[g]
            album.genres.append(genre)
        #on peut désormais ajouter l'album complet à la db
        db.session.add(album)
    db.session.commit()

    #creation de tous les genres

    #creation de tous les albums

@manager.command
def syncdb():
    ''' Creates all missing tables. '''
    db.create_all()

@manager.command
def newuser(username, password):
    '''Adds a new user.'''
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = User(username=username, password=m.hexdigest())
    db.session.add(u)
    db.session.commit()

@manager.command
def passwd(username,password):
    from .models import load_user
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = load_user(username)
    u.password = m.hexdigest()
    db.session.commit()
