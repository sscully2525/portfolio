#!/bin/bash

# Sean's Portfolio & AI Projects Launcher
echo "🚀 Sean Scully's Portfolio & AI Projects"
echo "=========================================="
echo ""

# Function to launch portfolio
launch_portfolio() {
    echo "🌐 Starting Portfolio Website..."
    echo "Opening http://localhost:8000"
    python3 -m http.server 8000 &
    sleep 2
    xdg-open http://localhost:8000 || open http://localhost:8000 || start http://localhost:8000
}

# Function to launch document analyzer
launch_document_analyzer() {
    echo "📄 Starting Smart Document Analyzer..."
    cd projects/document-analyzer || exit
    pip install -q -r requirements.txt
    streamlit run app.py &
    cd ../..
}

# Function to launch image studio
launch_image_studio() {
    echo "🎨 Starting AI Image Studio..."
    cd projects/ai-image-studio || exit
    pip install -q -r requirements.txt
    python app.py &
    cd ../..
}

# Function to launch predictive dashboard
launch_predictive_dashboard() {
    echo "📊 Starting Predictive Analytics Dashboard..."
    cd projects/predictive-dashboard || exit
    pip install -q -r requirements.txt
    streamlit run app.py &
    cd ../..
}

# Main menu
echo "What would you like to launch?"
echo ""
echo "1) 🌐 Portfolio Website (localhost:8000)"
echo "2) 📄 Smart Document Analyzer"
echo "3) 🎨 AI Image Studio"
echo "4) 📊 Predictive Analytics Dashboard"
echo "5) 🚀 Launch ALL projects"
echo "6) ❌ Exit"
echo ""

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        launch_portfolio
        ;;
    2)
        launch_document_analyzer
        ;;
    3)
        launch_image_studio
        ;;
    4)
        launch_predictive_dashboard
        ;;
    5)
        echo "🚀 Launching all projects..."
        launch_portfolio
        sleep 2
        launch_document_analyzer
        sleep 2
        launch_image_studio
        sleep 2
        launch_predictive_dashboard
        echo ""
        echo "✅ All projects launched!"
        echo "Portfolio: http://localhost:8000"
        ;;
    6)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "✅ Project launched successfully!"
echo "Press Ctrl+C to stop"
wait
