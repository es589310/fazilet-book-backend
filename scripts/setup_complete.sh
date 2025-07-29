#!/bin/bash

# Tam Django setup script
echo "🚀 Django Kitab Satış Saytı Setup"
echo "=================================="

# 1. Virtual environment yarat
echo "1. Virtual environment yaradılır..."
python -m venv venv

# 2. Virtual environment aktivasiya təlimatları
echo ""
echo "2. Virtual environment aktivasiya edin:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   venv\\Scripts\\activate"
else
    echo "   source venv/bin/activate"
fi

echo ""
echo "3. Paketləri quraşdırın:"
echo "   pip install -r requirements.txt"

echo ""
echo "4. Environment variables quraşdırın:"
echo "   .env faylını redaktə edin"

echo ""
echo "5. Database migration:"
echo "   python scripts/create_migrations.py"

echo ""
echo "6. Sample data əlavə edin:"
echo "   python scripts/create_sample_data.py"

echo ""
echo "7. Server-i işə salın:"
echo "   python scripts/run_server.py"

echo ""
echo "8. API-ni test edin:"
echo "   python scripts/test_api.py"

echo ""
echo "🎯 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://127.0.0.1:8000"
echo "   Admin:    http://127.0.0.1:8000/admin"
echo "   API:      http://127.0.0.1:8000/api"

echo ""
echo "✅ Setup tamamlandı!"
