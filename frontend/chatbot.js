/**
 * AI Chatbot Assistant for LETS GO Bus Service
 * Provides quick options and intelligent responses
 */

class ChatbotAssistant {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.init();
    }

    init() {
        // Don't show on login/register pages
        const currentPage = window.location.pathname;
        if (currentPage.includes('login.html') || currentPage.includes('register.html')) {
            return;
        }

        this.render();
        this.attachEventListeners();
        this.addWelcomeMessage();
    }

    render() {
        const chatbotHTML = `
            <div id="chatbot-container">
                <!-- Chat Toggle Button -->
                <button id="chatbot-toggle" class="chatbot-toggle">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="white">
                        <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
                    </svg>
                    <span class="chatbot-badge">!</span>
                </button>

                <!-- Chat Window -->
                <div id="chatbot-window" class="chatbot-window hidden">
                    <!-- Header -->
                    <div class="chatbot-header">
                        <div class="chatbot-header-info">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                                <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
                            </svg>
                            <div>
                                <h4>LETS GO Assistant</h4>
                                <span class="chatbot-status">Online</span>
                            </div>
                        </div>
                        <button id="chatbot-close" class="chatbot-close">&times;</button>
                    </div>

                    <!-- Messages Area -->
                    <div id="chatbot-messages" class="chatbot-messages">
                        <!-- Messages will be added here -->
                    </div>

                    <!-- Quick Options -->
                    <div id="chatbot-quick-options" class="chatbot-quick-options">
                        <button class="quick-option" data-action="search_bus">🔍 Search Bus</button>
                        <button class="quick-option" data-action="how_to_book">📋 How to Book</button>
                        <button class="quick-option" data-action="search_route">🗺️ Search Route</button>
                        <button class="quick-option" data-action="my_bookings">🎫 My Bookings</button>
                        <button class="quick-option" data-action="contact_support">📞 Contact Support</button>
                    </div>

                    <!-- Input Area -->
                    <div class="chatbot-input-area">
                        <input 
                            type="text" 
                            id="chatbot-input" 
                            class="chatbot-input" 
                            placeholder="Ask me anything..."
                            autocomplete="off"
                        >
                        <button id="chatbot-send" class="chatbot-send">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
        this.addStyles();
    }

    addStyles() {
        const styles = `
            <style>
                /* Chatbot Container */
                #chatbot-container {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 10000;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }

                /* Toggle Button */
                .chatbot-toggle {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    position: relative;
                }

                .chatbot-toggle:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }

                .chatbot-badge {
                    position: absolute;
                    top: -5px;
                    right: -5px;
                    background: #ff4757;
                    color: white;
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 14px;
                    font-weight: bold;
                    animation: pulse 2s infinite;
                }

                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                }

                /* Chat Window */
                .chatbot-window {
                    position: absolute;
                    bottom: 80px;
                    right: 0;
                    width: 380px;
                    height: 550px;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    transition: all 0.3s ease;
                    animation: slideIn 0.3s ease;
                }

                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                .chatbot-window.hidden {
                    display: none;
                }

                /* Header */
                .chatbot-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .chatbot-header-info {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }

                .chatbot-header h4 {
                    margin: 0;
                    font-size: 16px;
                    font-weight: 600;
                }

                .chatbot-status {
                    font-size: 12px;
                    opacity: 0.9;
                }

                .chatbot-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 28px;
                    cursor: pointer;
                    padding: 0;
                    width: 30px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    transition: background 0.3s;
                }

                .chatbot-close:hover {
                    background: rgba(255, 255, 255, 0.2);
                }

                /* Messages Area */
                .chatbot-messages {
                    flex: 1;
                    padding: 15px;
                    overflow-y: auto;
                    background: #f8f9fa;
                }

                .message {
                    margin-bottom: 15px;
                    display: flex;
                    animation: messageIn 0.3s ease;
                }

                @keyframes messageIn {
                    from {
                        opacity: 0;
                        transform: translateY(10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                .message.bot {
                    justify-content: flex-start;
                }

                .message.user {
                    justify-content: flex-end;
                }

                .message-content {
                    max-width: 80%;
                    padding: 12px 16px;
                    border-radius: 15px;
                    font-size: 14px;
                    line-height: 1.5;
                }

                .message.bot .message-content {
                    background: white;
                    color: #333;
                    border-bottom-left-radius: 5px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }

                .message.user .message-content {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-bottom-right-radius: 5px;
                }

                /* Quick Options */
                .chatbot-quick-options {
                    padding: 10px 15px;
                    background: white;
                    border-top: 1px solid #eee;
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                }

                .quick-option {
                    background: #f0f2f5;
                    border: 1px solid #ddd;
                    padding: 8px 12px;
                    border-radius: 20px;
                    font-size: 13px;
                    cursor: pointer;
                    transition: all 0.3s;
                    white-space: nowrap;
                }

                .quick-option:hover {
                    background: #667eea;
                    color: white;
                    border-color: #667eea;
                    transform: translateY(-2px);
                }

                /* Input Area */
                .chatbot-input-area {
                    padding: 15px;
                    background: white;
                    border-top: 1px solid #eee;
                    display: flex;
                    gap: 10px;
                }

                .chatbot-input {
                    flex: 1;
                    padding: 12px 15px;
                    border: 1px solid #ddd;
                    border-radius: 25px;
                    font-size: 14px;
                    outline: none;
                    transition: border-color 0.3s;
                }

                .chatbot-input:focus {
                    border-color: #667eea;
                }

                .chatbot-send {
                    width: 45px;
                    height: 45px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: transform 0.3s;
                }

                .chatbot-send:hover {
                    transform: scale(1.1);
                }

                /* Typing Indicator */
                .typing-indicator {
                    display: flex;
                    gap: 5px;
                    padding: 12px 16px;
                    background: white;
                    border-radius: 15px;
                    border-bottom-left-radius: 5px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    width: fit-content;
                }

                .typing-indicator span {
                    width: 8px;
                    height: 8px;
                    background: #667eea;
                    border-radius: 50%;
                    animation: typing 1.4s infinite;
                }

                .typing-indicator span:nth-child(2) {
                    animation-delay: 0.2s;
                }

                .typing-indicator span:nth-child(3) {
                    animation-delay: 0.4s;
                }

                @keyframes typing {
                    0%, 60%, 100% {
                        transform: translateY(0);
                    }
                    30% {
                        transform: translateY(-10px);
                    }
                }

                /* Responsive */
                @media (max-width: 480px) {
                    #chatbot-container {
                        bottom: 10px;
                        right: 10px;
                    }

                    .chatbot-window {
                        width: calc(100vw - 20px);
                        height: 70vh;
                        bottom: 70px;
                    }

                    .chatbot-toggle {
                        width: 55px;
                        height: 55px;
                    }
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
    }

    attachEventListeners() {
        const toggleBtn = document.getElementById('chatbot-toggle');
        const closeBtn = document.getElementById('chatbot-close');
        const chatWindow = document.getElementById('chatbot-window');
        const sendBtn = document.getElementById('chatbot-send');
        const input = document.getElementById('chatbot-input');
        const quickOptions = document.querySelectorAll('.quick-option');

        // Toggle chat window
        toggleBtn.addEventListener('click', () => {
            this.isOpen = !this.isOpen;
            chatWindow.classList.toggle('hidden', !this.isOpen);
            if (this.isOpen) {
                input.focus();
            }
        });

        // Close chat
        closeBtn.addEventListener('click', () => {
            this.isOpen = false;
            chatWindow.classList.add('hidden');
        });

        // Send message on button click
        sendBtn.addEventListener('click', () => this.sendMessage());

        // Send message on Enter key
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Quick option clicks
        quickOptions.forEach(option => {
            option.addEventListener('click', () => {
                const action = option.dataset.action;
                this.handleQuickAction(action);
            });
        });
    }

    addWelcomeMessage() {
        setTimeout(() => {
            this.addBotMessage("Hi! 👋 I'm your LETS GO assistant. How can I help you today?");
        }, 500);
    }

    sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();

        if (!message) return;

        this.addUserMessage(message);
        input.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        // Process and respond
        setTimeout(() => {
            this.removeTypingIndicator();
            const response = this.getBotResponse(message);
            this.addBotMessage(response);
        }, 800 + Math.random() * 500);
    }

    handleQuickAction(action) {
        const actions = {
            'search_bus': {
                user: 'Search Bus',
                bot: 'To search for a bus:\n\n1️⃣ Go to the Home page\n2️⃣ Enter your departure city\n3️⃣ Enter your destination\n4️⃣ Select your travel date\n5️⃣ Click "Search"\n\nYou\'ll see all available buses with timings and prices! 🚌'
            },
            'how_to_book': {
                user: 'How to Book Bus',
                bot: 'Booking a bus ticket is easy:\n\n1️⃣ Search for your route\n2️⃣ Select a bus from the results\n3️⃣ Choose your seats\n4️⃣ Enter passenger details\n5️⃣ Make payment via UPI\n6️⃣ Download your e-ticket\n\nYour ticket will also be saved in "My Bookings"! 🎫'
            },
            'search_route': {
                user: 'Search Route',
                bot: 'To search for routes:\n\n🗺️ We operate on multiple routes in and around Pune\n\nPopular routes include:\n• Pune → Mumbai\n• Pune → Nashik\n• Pune → Aurangabad\n• Pune → Kolhapur\n\nCheck the Home page for all available routes! 🚌'
            },
            'my_bookings': {
                user: 'My Bookings',
                bot: 'To view your bookings:\n\n📋 Click on "My Booking" in the navigation menu\n\nYou\'ll see:\n• Your recent 5 bookings\n• Booking status\n• Seat details\n• Option to download PDF tickets\n\nYou can also cancel pending bookings from there! 🎫'
            },
            'contact_support': {
                user: 'Contact Support',
                bot: 'Need help? Here\'s how to reach us:\n\n📧 Email: support@letsgo.com\n📞 Phone: +91 1800-123-4567\n💬 Live Chat: Use this chat!\n\nSupport Hours:\nMon-Sat: 9 AM - 9 PM\nSunday: 10 AM - 6 PM\n\nWe\'re here to help! 😊'
            }
        };

        const actionData = actions[action];
        if (actionData) {
            this.addUserMessage(actionData.user);
            this.showTypingIndicator();
            setTimeout(() => {
                this.removeTypingIndicator();
                this.addBotMessage(actionData.bot);
            }, 600);
        }
    }

    getBotResponse(message) {
        const lowerMessage = message.toLowerCase();

        // Keyword-based responses
        const responses = [
            {
                keywords: ['hello', 'hi', 'hey', 'greetings'],
                response: "Hello! 👋 Welcome to LETS GO Bus Service. How can I assist you today?"
            },
            {
                keywords: ['book', 'booking', 'reserve', 'ticket'],
                response: "To book a ticket:\n\n1. Go to Home page\n2. Enter your route (From → To)\n3. Select travel date\n4. Choose a bus\n5. Pick your seats\n6. Enter passenger details\n7. Complete payment\n\nYour e-ticket will be generated instantly! 🎫"
            },
            {
                keywords: ['search', 'find', 'look for'],
                response: "To search for buses:\n\n🔍 Use the search form on the Home page\n• Enter departure city\n• Enter destination\n• Select travel date\n• Click Search\n\nYou'll see all available buses with real-time seat availability! 🚌"
            },
            {
                keywords: ['cancel', 'cancellation', 'refund'],
                response: "To cancel a booking:\n\n1. Go to \"My Bookings\"\n2. Find your booking\n3. Click \"Cancel\" (only for pending bookings)\n\n⚠️ Cancellation policy:\n• Free cancellation within 24 hours\n• 50% refund after 24 hours\n• No refund after 48 hours of journey"
            },
            {
                keywords: ['payment', 'pay', 'upi', 'money'],
                response: "We accept UPI payments:\n\n💳 Supported apps:\n• Google Pay\n• PhonePe\n• Paytm\n• BHIM\n• Any UPI app\n\nSimply scan the QR code or use the UPI ID provided during checkout. It's secure and instant! 🔒"
            },
            {
                keywords: ['route', 'destination', 'where', 'go'],
                response: "Our popular routes include:\n\n🗺️ Pune ↔ Mumbai\n🗺️ Pune ↔ Nashik\n🗺️ Pune ↔ Aurangabad\n🗺️ Pune ↔ Kolhapur\n🗺️ Pune → Shirdi\n\nCheck the Home page for all available routes and schedules! 🚌"
            },
            {
                keywords: ['seat', 'seats', 'window', 'berth'],
                response: "Seat selection is easy:\n\n💺 Green = Available (click to select)\n🔴 Red = Booked (unavailable)\n\nYou can:\n• Choose specific seats\n• See seat layout\n• Select multiple seats\n• See fare based on seats\n\nPremium seats available on select buses! ✨"
            },
            {
                keywords: ['contact', 'support', 'help', 'call', 'email'],
                response: "Contact us anytime:\n\n📧 support@letsgo.com\n📞 1800-123-4567 (Toll-free)\n💬 Use this chat for instant help\n\nSupport Hours:\nMon-Sat: 9 AM - 9 PM\nSunday: 10 AM - 6 PM"
            },
            {
                keywords: ['price', 'fare', 'cost', 'how much'],
                response: "Our fares are competitive and transparent:\n\n💰 Base fare starts from ₹299\n• Distance-based pricing\n• No hidden charges\n• GST included\n\nThe final price is shown before booking. Premium buses may cost slightly more! ✨"
            },
            {
                keywords: ['time', 'duration', 'how long', 'reach'],
                response: "Travel times vary by route:\n\n⏱️ Pune → Mumbai: ~3-4 hours\n⏱️ Pune → Nashik: ~4-5 hours\n⏱️ Pune → Aurangabad: ~5-6 hours\n⏱️ Pune → Kolhapur: ~4-5 hours\n\nExact duration shown during booking! 🚌"
            },
            {
                keywords: ['amenities', 'facilities', 'ac', 'wifi', 'charging'],
                response: "Our buses offer:\n\n✨ Air Conditioning\n✨ Charging Points\n✨ Reading Lights\n✨ Reclining Seats\n✨ Water Bottles\n✨ GPS Tracking\n\nAmenities vary by bus type. Check bus details before booking! 🚌"
            },
            {
                keywords: ['download', 'ticket', 'pdf', 'print'],
                response: "To download your ticket:\n\n1. Go to \"My Bookings\"\n2. Find your confirmed booking\n3. Click \"PDF\" button\n4. Save or print the ticket\n\nYou can also show the e-ticket on your phone during boarding! 📱"
            },
            {
                keywords: ['admin', 'dashboard', 'stats'],
                response: "The Admin Dashboard shows:\n\n📊 Total Revenue (from recent bookings)\n📊 Total Bookings count\n📊 Recent bookings list with passenger details\n📊 Filter by month/year\n\nAccess it via the \"Admin\" menu option! 🔐"
            },
            {
                keywords: ['thank', 'thanks', 'great', 'awesome', 'helpful'],
                response: "You're welcome! 😊 Happy to help!\n\nHave a great journey with LETS GO! 🚌\n\nAnything else I can assist you with?"
            },
            {
                keywords: ['bye', 'goodbye', 'see you'],
                response: "Goodbye! 👋\n\nThank you for choosing LETS GO Bus Service!\n\nHave a safe and pleasant journey! 🚌✨"
            }
        ];

        // Find matching response
        for (const item of responses) {
            if (item.keywords.some(keyword => lowerMessage.includes(keyword))) {
                return item.response;
            }
        }

        // Default response for unmatched queries
        const defaultResponses = [
            "I'm not sure I understand. Could you please rephrase?\n\nYou can ask me about:\n• Booking tickets\n• Searching for buses\n• Cancellations\n• Payment methods\n• Routes and timings\n\nOr click on the quick options below! 👇",
            "That's an interesting question! Let me help you with something I know about:\n\n🚌 Bus bookings\n🎫 Ticket management\n🗺️ Routes\n💳 Payments\n❓ Cancellations\n\nWhat would you like to know?",
            "I want to help, but I need more details!\n\nTry asking about:\n• How to book a ticket\n• Available routes\n• Payment options\n• Cancellation policy\n• Your bookings\n\nOr use the quick action buttons! 😊"
        ];

        return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
    }

    addUserMessage(text) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageHTML = `
            <div class="message user">
                <div class="message-content">${this.escapeHtml(text)}</div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        this.scrollToBottom();
    }

    addBotMessage(text) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const formattedText = text.replace(/\n/g, '<br>');
        const messageHTML = `
            <div class="message bot">
                <div class="message-content">${formattedText}</div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatbot-messages');
        const indicatorHTML = `
            <div class="message bot" id="typing-indicator">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', indicatorHTML);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chatbot-messages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatbotAssistant();
});
