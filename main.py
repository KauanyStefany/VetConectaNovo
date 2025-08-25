from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from routes.admin import categoria_artigo_routes, chamado_routes, comentario_admin_routes, denuncia_admin_routes, resposta_chamado_routes, verificação_crmv_routes
from routes.publico import public_routes
from routes.tutor import comentario_tutor_routes, curtida_artigo_tutor_routes, curtida_feed_tutor_routes, denuncia_tutor_routes, postagem_feed_routes, seguida_tutor_routes
from routes.veterinario import comentario_veterinario_routes, estatisticas_routes, postagem_artigo_routes


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public_routes.router)
app.include_router(categoria_artigo_routes.router, prefix="/admin", tags=["admin"])
app.include_router(chamado_routes.router, prefix="/admin", tags=["admin"])
app.include_router(comentario_admin_routes.router, prefix="/admin", tags=["admin"])
app.include_router(denuncia_admin_routes.router, prefix="/admin", tags=["admin"])
app.include_router(resposta_chamado_routes.router, prefix="/admin", tags=["admin"])
app.include_router(verificação_crmv_routes.router, prefix="/admin", tags=["admin"])

app.include_router(comentario_tutor_routes.router, prefix="/tutor", tags=["tutor"])
app.include_router(curtida_artigo_tutor_routes.router, prefix="/tutor", tags=["tutor"])
app.include_router(curtida_feed_tutor_routes.router, prefix="/tutor", tags=["tutor"])
app.include_router(denuncia_tutor_routes.router, prefix="/tutor", tags=["tutor"])
app.include_router(postagem_feed_routes.router, prefix="/tutor", tags=["tutor"])
app.include_router(seguida_tutor_routes.router, prefix="/tutor", tags=["tutor"]) #só o tutor pode seguir? E o veterinario não pode seguir outro veterinario?

app.include_router(comentario_veterinario_routes.router, prefix="/veterinario", tags=["veterinario"])
# app.include_router(denuncia_veterinario_routes.router, prefix="/veterinario", tags=["veterinario"])
app.include_router(postagem_artigo_routes.router, prefix="/veterinario", tags=["veterinario"])
# app.include_router(seguida_veterinario_routes.router, prefix="/veterinario", tags=["veterinario"]) 
app.include_router(estatisticas_routes.router, prefix="/veterinario", tags=["veterinario"])


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)