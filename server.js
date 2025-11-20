const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcrypt');

const app = express();
app.use(cors());
app.use(express.json());

// Connect to MongoDB
mongoose.connect('mongodb://127.0.0.1:27017/disease_radar', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
.then(() => console.log('✅ Connected to MongoDB'))
.catch(err => console.error('❌ MongoDB connection error:', err));

const UserSchema = new mongoose.Schema({
    name: String,
    contact: String,
    password: String
});

const User = mongoose.model('User', UserSchema);

// Signup route
app.post('/signup', async (req, res) => {
    const { name, contact, password } = req.body;

    const existing = await User.findOne({ contact });
    if (existing) return res.json({ success: false, message: 'User already exists' });

    const hashed = await bcrypt.hash(password, 10);
    const user = new User({ name, contact, password: hashed });
    await user.save();

    res.json({ success: true });
});

// Login route
app.post('/login', async (req, res) => {
    const { contact, password } = req.body;

    const user = await User.findOne({ contact });
    if (!user) return res.json({ success: false });

    const match = await bcrypt.compare(password, user.password);
    if (!match) return res.json({ success: false });

    res.json({ success: true });
});

app.listen(3000, () => console.log('🚀 Server running on http://localhost:3000'));
