import redis
from app.config import settings

# Testar conexão
try:
    r = redis.from_url(settings.redis_url)
    r.ping()
    print("✅ Redis conectado com sucesso!")
    
    # Testar set/get
    r.set("teste", "funcionou!")
    valor = r.get("teste")
    print(f"✅ Teste set/get: {valor.decode()}")
    
    r.delete("teste")
    print("✅ Redis está funcionando perfeitamente!")
    
except Exception as e:
    print(f"❌ Erro ao conectar no Redis: {e}")