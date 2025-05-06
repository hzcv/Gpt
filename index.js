const Insta = require('@androz2091/insta.js');
const { keep_alive } = require("./keep_alive");
require('dotenv').config();
const fetch = require("node-fetch");
const client = new Insta.Client();

// Set your own username(s) here
const OWNER_USERNAMES = ['your_username'];

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

client.on('connected', () => {
    console.log(`✅ Logged in as ${client.user.username}`);
});

client.on('messageCreate', async (message) => {
    if (message.author.id === client.user.id) return; // ignore own messages
    if (!message.chat.isGroup) return;                // only in groups
    if (OWNER_USERNAMES.includes(message.author.username)) return; // ignore owners

    try {
        await message.markSeen();
        await delay(2000); // wait 2 sec to appear human

        // 1. Tag and custom reply
        const tagReply = `@${message.author.username} Oy msg mt kr yrr`;
        await message.reply(tagReply);

        // 2. Chatbot reply using Affiliate+ API
        const res = await fetch(`https://api.affiliateplus.xyz/api/chatbot?message=${encodeURIComponent(message.content)}&botname=${client.user.username}&ownername=Diwas Atreya`);
        const json = await res.json();

        if (json.message) {
            await delay(1000); // short pause before second reply
            await message.reply(json.message);
        }

        console.log(`💬 Replied to ${message.author.username} in ${message.chat.name}`);
    } catch (err) {
        console.error("❌ Error:", err);
    }
});

client.login(process.env.INSTA_USER, process.env.INSTA_PASS);
