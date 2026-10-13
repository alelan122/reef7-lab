/* My Daily Peak (Full Peak / PeakMag)
 * Client-side companion program. All progress lives in the visitor's browser
 * (localStorage); the page itself stays fully cacheable by Shopify's CDN.
 * Optional: goal/profile tags are pushed to Shopify Customers through the
 * theme's native customer form (only with explicit marketing consent).
 */
(function () {
  'use strict';

  var KEY = 'fp-reset-v1';
  var CORE_DAYS = 45;
  var MAX_DAYS = 90;
  var CAPS_PER_BOTTLE = 90;   // label: 1 capsule a day, optional 2nd at a different time, max 2
  var METRICS = [
    { id: 'sleep', label: 'Sleep quality', low: 'Restless', high: 'Deep' },
    { id: 'calm', label: 'Calm', low: 'Tense', high: 'Relaxed' },
    { id: 'energy', label: 'Energy', low: 'Drained', high: 'Steady' }
  ];

  var PHASES = [
    // Phases describe what the person DOES, not results they are promised (no typical-results claims).
    { id: 1, from: 1, to: 7, name: 'Start', text: 'Take your capsule every day and learn the routine.' },
    { id: 2, from: 8, to: 21, name: 'Build', text: 'Add one small habit at a time, on top of your daily capsule.' },
    { id: 3, from: 22, to: 45, name: 'Keep', text: 'Your routine starts to feel automatic. Keep showing up.' },
    { id: 4, from: 46, to: 90, name: 'Stay', text: 'Keep the habits that helped you most, with a new plan for each day.', bonus: true }
  ];

  var ICONS = {
    sleep: '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
    stress: '<path d="M2 12c3-4 5-4 8 0s5 4 8 0c1.3-1.7 2.7-2 4-2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M2 17c3-4 5-4 8 0s5 4 8 0c1.3-1.7 2.7-2 4-2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity=".45"/>',
    energy: '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    recovery: '<path d="M3 12h4l2-5 4 10 2-5h6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    lock: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" stroke-width="2"/>',
    box: '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M3 7.5 12 12l9-4.5M12 12v9" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
  };

  var GOALS = {
    sleep: { label: 'Sleep deeper', sub: 'Switch off at night, wake up rested' },
    stress: { label: 'Calm my body', sub: 'A calmer, more balanced day' },
    energy: { label: 'Steady energy', sub: 'Calm and sharp, no afternoon crash' },
    recovery: { label: 'Recover faster', sub: 'Training, sore and tense muscles' }
  };

  // Onboarding questions. Rule: every question either changes something the customer sees in the plan,
  // or gives us data we use for ads and the product page. "Us-only" questions are optional and come last.
  var AGES = [['u30', '18–29'], ['30-44', '30–44'], ['45-59', '45–59'], ['60plus', '60+']];
  var SEXES = [['f', 'Woman'], ['m', 'Man'], ['x', 'Prefer not to say']];
  // Starting point, with a one-line description so people pick the right one fast.
  var FEELS = [
    ['wired', 'Wired but tired', 'Exhausted, but can\'t switch off'],
    ['drained', 'Drained', 'Low energy most of the day'],
    ['tense', 'Tense', 'Tight body, busy mind'],
    ['normal', 'Normal', 'Fine, but could be better']
  ];
  // Optional, multi-select. Segments from the Desire Research.
  var EXTRAS = [['cramps', 'Night cramps or restless legs'], ['jaw', 'Jaw clenching at night'], ['peri', 'Perimenopause']];
  // Past experience with magnesium = the objection we need to answer first.
  var TRIED = [['first', 'No, this is my first time'], ['nowork', 'Yes, but I did not notice much'], ['stomach', 'Yes, but it upset my stomach']];
  // Meal anchor: tying a new habit to an existing one is the best-studied way to make it stick.
  var MEALS = [['breakfast', 'Breakfast'], ['lunch', 'Lunch'], ['dinner', 'Dinner']];
  // One-tap examples for "your why", per goal (people freeze in front of an empty box).
  var WHY_EXAMPLES = {
    // The deeper reason (people, identity, moments), not the goal restated.
    sleep: ['Be present with my family, not just there', 'Wake up and actually want to start my day', 'Stop dreading bedtime'],
    stress: ['Be the calm one at home, not the snappy one', 'Enjoy my evenings instead of replaying the day', 'Feel like myself again'],
    energy: ['Keep up with my kids after work', 'Finally do the things I keep putting off', 'Feel sharp at work without three coffees'],
    recovery: ['Train hard and still feel good the next day', 'Hit my goals without getting sidelined', 'Stay active for years, not weeks']
  };
  var OB_STEPS = 5;

  var BOTTLES = [['1', '1 bottle'], ['2', '2 bottles'], ['4', '4 bottles']];
  var CAPS = [['1', '1 a day (suggested start)'], ['2', '2 a day, at different times']];
  var STARTS = [['wait', "Not yet, it's on its way"], ['0', 'Today'], ['1', 'Yesterday'], ['3', 'A few days ago'], ['7', 'About a week ago']];

  // One small habit per day: 5 per phase per goal, rotating inside the phase.
  var HABITS = {
    sleep: [
      ['Pick one fixed wake-up time for this week, weekends included.',
        'Last coffee before 2 PM today.',
        'Dim the lights at home 60 minutes before bed.',
        'Phone out of the bedroom tonight.',
        "Write tomorrow's top 3 tasks before bed so your head can let go."],
      ['Keep your bedroom cool tonight, around 65–68°F.',
        'Get 10 minutes of daylight within an hour of waking.',
        'In bed, try 4 rounds of 4-7-8 breathing.',
        'Before sleep, unclench: lips together, teeth apart, shoulders down.',
        'Swap the last scroll of the day for 10 pages of a book.'],
      ['Notice your new baseline: how fast did you fall asleep last night?',
        'Keep the wake-up time. It is the anchor for everything else.',
        'If you nap, keep it under 20 minutes and before 3 PM.',
        "Swap tonight's glass of wine for a wind-down ritual: herbal tea, dim lights, 10 quiet minutes.",
        'Build your shutdown ritual: same 3 steps, same order, every night.']
    ],
    stress: [
      ['Three slow breaths before you open email or messages.',
        'A 10-minute walk outside, no headphones.',
        'Cap caffeine at 2 cups today.',
        "Write down what's weighing on you most, then one small next step.",
        'A 2-minute break for every 90 minutes of focused work.'],
      ['3 minutes of box breathing (4-4-4-4) mid-afternoon.',
        'Eat one magnesium-rich food today: spinach, pumpkin seeds, almonds or dark chocolate.',
        'Mute non-essential notifications for the rest of the day.',
        'In bed, a slow body scan: relax your jaw, neck, shoulders and hands, one at a time.',
        "Say no to one thing that doesn't matter this week."],
      ['Check in with yourself: what bothers you less than on Day 1?',
        'Plan one fully offline hour this weekend.',
        'Move your body for 20 minutes, any way you like.',
        'Aim for 8 glasses of water today.',
        'Thank one person today. A quick reset for your mood.']
    ],
    energy: [
      ['A full glass of water before your first coffee.',
        'Push your first coffee 60–90 minutes after waking.',
        'Protein at breakfast today.',
        '5 minutes of daylight before noon.',
        'Get up and move for 2 minutes every hour.'],
      ['Swap the afternoon sugar snack for nuts or fruit.',
        'Eat one magnesium-rich food today: spinach, pumpkin seeds, almonds or black beans.',
        'A 10-minute walk after lunch to skip the afternoon dip.',
        'Lights out 30 minutes earlier tonight.',
        'Add a pinch of salt and a squeeze of lemon to your morning water.'],
      ['Notice your energy at 3 PM and compare it to Day 1.',
        "Keep the coffee cut-off you've built.",
        "Plan tomorrow's meals so you're not running on snacks.",
        'A short workout today. 15 minutes is enough.',
        'Protect your sleep window tonight. Energy is built the night before.']
    ],
    recovery: [
      ['16 oz of water within an hour after training.',
        'Add 5 minutes of mobility work at the end of your session.',
        'Protein within 2 hours of your workout.',
        'On rest days, walk 20–30 minutes.',
        'Aim for 7+ hours of sleep tonight. It is your #1 recovery tool.'],
      ['Sweaty day? Water plus a pinch of salt.',
        'Foam roll or stretch the muscles you trained today.',
        'One full rest day this week. Actually rest.',
        'Eat one magnesium-rich food today: pumpkin seeds, spinach, almonds or dark chocolate.',
        '3 minutes of slow nasal breathing after training to cool down.'],
      ['Rate your soreness today versus Day 1.',
        "Log one strength number. You're building, not just recovering.",
        'Warm up for 5 full minutes before your session.',
        'Keep the post-workout protein habit.',
        'Plan next week with a lighter day built in.']
    ]
  };

  var MAINTAIN = [
    'Keep your anchor: same wake-up time, every day.',
    'Which 3 habits made the biggest difference? Keep those, drop the rest.',
    'One magnesium-rich meal today.',
    'Is your coffee cut-off still in place?',
    '10 minutes of daylight before noon.',
    'Screen-free last 30 minutes of the day.',
    'Move for 20 minutes today.',
    'Write down one win from this week.'
  ];

  // Daily line under the title. Full Peak voice: climbing, steady, never preachy.
  var QUOTES = [
    'Every peak is climbed one step at a time.',
    "You don't have to feel it yet. You just have to show up.",
    'Small steps. Higher ground.',
    'Consistency is quieter than motivation, and stronger.',
    "Today counts, even if it doesn't feel like it.",
    'The view gets better the higher you go.',
    'Rest is part of the climb.',
    'Progress, not perfection.',
    'Give your future self something to thank you for.',
    'One good day is a start. A good week is a pattern.',
    "Calm is a skill. You're practicing it.",
    'Strong days are built in the quiet hours.',
    'Show up for yourself the way you show up for others.',
    "Peaks aren't reached in a day. Neither are habits.",
    'Slow is still forward.',
    'Keep the promise you made on Day 1.',
    "You're higher than you were yesterday.",
    'Energy is built the night before.',
    'Little by little, a little becomes a lot.',
    'Reach your peak. Then find the next one.'
  ];

  // Earned by number of check-ins, not calendar days: consistency is what we reward.
  var BADGES = [
    { n: 3, name: 'Base camp' }, { n: 7, name: 'First ridge' }, { n: 14, name: 'Above the clouds' },
    { n: 21, name: 'Second wind' }, { n: 30, name: 'Thin air' }, { n: 45, name: 'Full Peak' },
    { n: 60, name: 'Ridge walker' }, { n: 90, name: 'Summit' }
  ];

  // "Science, simply": Huberman-style practical protocols, 6th-grade level. Lifestyle science only, the product is
  // not the topic here. Sources: circadian light research, Balban et al. 2023 (Cell Reports Medicine, cyclic sighing),
  // caffeine half-life (~5 h), Haghayegh et al. 2019 (warm bath before bed), post-meal walking and glucose studies,
  // alcohol and REM sleep research, Lally et al. 2010 (habit formation). Hedged where evidence is still growing.
  var INSIGHTS = {
    3: ['The 10-minute habit that sets your whole day', 'Go outside for 5 to 10 minutes within an hour of waking, longer if it is cloudy. Morning light sets your body clock, which decides when you feel alert and, about 14 to 16 hours later, when you feel sleepy. Through a window it is much dimmer, so step outside.'],
    6: ['The fastest off switch you own', 'Breathe in twice through your nose, then let out one long breath through your mouth. Stanford researchers found that 5 minutes a day of this "cyclic sighing" lifted mood more than meditation. Long exhales are a direct line to your nervous system\'s brake pedal.'],
    10: ['Your 2 PM coffee is still awake at 7', 'Caffeine takes about 5 hours for half of it to leave your body, so half of a 2 PM coffee is still there at 7 PM. Set a cut-off 8 to 10 hours before bed. You can fall asleep fine and still sleep lighter.'],
    14: ['Sleep starts with a temperature drop', 'Your body temperature has to drop a little for you to fall asleep. Keep your bedroom cool, around 65 to 68°F. A warm shower 1 to 2 hours before bed helps too, because your body cools down fast afterward.'],
    18: ['Your ceiling lights are confusing your brain', 'Bright light at night tells your brain it is still daytime and pushes sleep later. In the evening, switch off ceiling lights and use a few low lamps instead. Your brain reads light from above as "sun".'],
    24: ['The one time that matters more than bedtime', 'The time you get up sets your rhythm more than the time you go to bed. Keep it within about an hour every day, weekends too. Sleepy evenings tend to follow steady mornings.'],
    29: ['The 10-minute walk your energy wants', 'A 10-minute walk after a meal helps your muscles use the sugar from that meal, which can mean steadier energy and fewer slumps. Movement during the day also tends to mean deeper sleep at night.'],
    34: ['The nightcap that steals your night', 'A drink can help you fall asleep faster, but it breaks up the second half of the night and cuts into dream (REM) sleep. If you drink, finish at least 3 hours before bed.'],
    38: ['The 20-minute reset for short nights', 'After a short night, a 10 to 20 minute rest lying down with a slow body scan can help you feel more restored. It is often called NSDR or yoga nidra. Eyes closed, breathe slowly, relax one body part at a time.'],
    43: ['Why 66 is the magic number', 'In a study on real habits, it took 66 days on average for a new habit to feel automatic, and missing one day did not ruin it. Keep the ones that clearly helped you. They are yours now.']
  };

  // "Magnesium, answered": the real questions customers ask (Desire Research), answered with strong but true
  // facts. The answer itself shows why the product is built the way it is. Sources: NIH ODS magnesium fact sheet;
  // Rosanoff et al. 2012 (48% of the US population below the EAR from food, NHANES 2005-06); Pickering et al. 2020
  // (stress and magnesium "vicious circle"); small 4-week study in students, 2x250 mg, lower serum cortisol (Belgrade);
  // Mah & Pitre 2021 (older adults fell asleep ~17 min faster, low-certainty evidence); EU Reg. 432/2012 authorised
  // claim on tiredness and fatigue; Uwitonze & Razzaque 2018 (vitamin D needs magnesium); Lally et al. 2010.
  // Structure/function wording; early evidence is labelled as such.
  var ANSWERS = {
    deficit: ['Half of America is running low', 'National nutrition surveys show that about 48% of Americans do not get enough magnesium from food. Not because they eat badly: white flour, processed food, stress, coffee and alcohol all quietly drain it. The early signs, like tiredness and weakness, are so easy to miss that most people never connect the dots. You just did.'],
    blood: ['Your blood test has a blind spot', 'Less than 1% of your magnesium lives in your blood. When you run low, your body borrows from your bones and muscles to keep that 1% looking perfect. So a "normal" test can hide empty stores. That is why topping up is a daily habit, not a one-time fix.'],
    stress: ['The loop that keeps you wired', 'Stress makes your body flush out magnesium. Less magnesium makes stress hit harder. Which makes you flush out more. Researchers call it a vicious circle, and it explains why stressful months seem to snowball. In a small 4-week study, magnesium lowered cortisol levels in students. A steady daily supply supports a calmer stress response, one day at a time.'],
    sleep: ['Why it is not a sleeping pill (and why that is good)', 'Melatonin tells your brain it is night. Magnesium does something different: it helps your muscles let go and supports the calming side of your nervous system, so your body can wind down on its own. In early studies of older adults, people fell asleep about 17 minutes faster on average. No knockout. No morning fog.'],
    energy: ['The spark plug in every cell', 'Your cells run on an energy molecule called ATP, but ATP cannot do anything until magnesium clicks into it. No magnesium, no usable energy. That is why Europe officially recognizes magnesium for helping reduce tiredness and fatigue. Energy that starts inside your cells, not in a can.'],
    sweat: ['Every workout has a hidden cost', 'Sweat carries magnesium out of your body, and hard training burns through more. Some researchers estimate athletes need 10 to 20% more. Magnesium also helps your muscles relax after they work. Train hard, top up, recover.'],
    vitd: ['Your vitamin D needs a partner', 'Vitamin D cannot do its job until magnesium switches it on. Without enough magnesium, it stays in a form your body cannot fully use. If you take vitamin D, magnesium is the other half of the team.'],
    meet8: ['One form is a guess. Eight is a team.', 'Most supplements bet everything on a single form of magnesium. Yours carries 8: fast ones like citrate, gentle ones like glycinate, energy-cycle ones like malate and aspartate, and slow, strong ones like oxide. Different partners, different speeds, one capsule. No guessing which one your body likes best.'],
    oxide: ['The "cheap" form we kept on purpose', 'Oxide gets a bad name online. But it packs the most magnesium into the smallest space, which keeps your capsule small, and it dissolves slowly, so it keeps going after the fast forms are done. In a blend, the slow lane is a feature, not a shortcut.'],
    stomach: ['The number one fear about magnesium', 'Most people worry it will send them running to the bathroom. That usually comes from big single doses. One capsule with a meal is the gentlest way to take it, and if you add a second, take it at a different time of day. Gentle and steady wins.'],
    coffee: ['Your coffee has a side effect nobody mentions', 'Caffeine and alcohol both make your kidneys flush out extra magnesium. Not a reason to give up your coffee. Just a reason your daily magnesium matters even more if coffee is part of your day.'],
    when1: ['The best time is the one you never miss', 'Morning or night both work. What matters is the same time every day, with a meal. Your body tops up slowly, so steady beats strong. Pick the meal you never skip, and you will never have to think about it again.'],
    when2: ['Two capsules? Split them.', 'Your body absorbs a bigger share of magnesium when it arrives in smaller amounts. So take one with breakfast and one with dinner, never both at once. Same total, more of it put to work.'],
    howlong: ['Why we will not promise you Day 3', 'Your body rebuilds its magnesium stores over weeks, not days. Some people notice small changes early, others later. Anyone who promises overnight results is guessing. Your plan does something better: it tracks your scores, so you see your own trend with your own eyes.'],
    stop: ['What happens if you stop?', 'Your body uses and loses magnesium every single day: through sweat, stress, coffee and simply living. It cannot bank it in your blood for later. Stop topping up, and your stores slowly drift back to where they started, especially for the 48% who do not get enough from food. The routine you built is what keeps you where you are now.'],
    whyours: ['Why not just any magnesium?', 'Most magnesium on the shelf is a single form, and it comes with nothing but a label. Yours is 8 forms in one capsule, plus a daily plan that knows your goal and tracks your progress. Switching means going back to guessing: which form, how much, and whether it is even working.'],
    daily: ['Built for every single day', 'Your body uses magnesium every day and cannot bank it in your blood for later. That is why it works as a daily habit, not a one-time fix. Stick to the label, and talk to your doctor first if you have kidney problems or take medication.']
  };
  // Questions closest to each goal come first.
  var GOAL_QS = {
    sleep: ['sleep', 'stress', 'energy', 'sweat', 'vitd'],
    stress: ['stress', 'sleep', 'energy', 'vitd', 'sweat'],
    energy: ['energy', 'stress', 'sweat', 'sleep', 'vitd'],
    recovery: ['sweat', 'energy', 'sleep', 'stress', 'vitd']
  };

  // "A thought for today": reflective and kind, different from the header quotes.
  var THOUGHTS = [
    'Notice one thing that felt a little easier this week. Small wins are still wins.',
    "You don't need a perfect day. You need a day you showed up for.",
    'Be as patient with your body as you would be with a good friend.',
    "Rest isn't something you earn. It's something you need.",
    'What helped you most yesterday? Do a little more of that today.',
    'Your pace is the right pace.',
    "Think of someone who'd be glad to see you feeling better. Today is for them too.",
    "Calm isn't a quiet day. It's how you move through a busy one.",
    'A good night starts with how you end your day.',
    "You've already done the hardest part. You started.",
    'Feeling better is rarely loud. Often it just looks like an easy, ordinary day.',
    'Take one slow breath before you scroll on. That counts.',
    'Some days are for climbing. Some are for catching your breath. Both move you forward.',
    'Tonight, think of one thing you are grateful for.',
    'Your body works for you all day long. Give it one kind thing back today.',
    'Progress you cannot see yet is still progress.',
    'When it feels slow, look at your chart, not the mirror.',
    'Every afternoon is a chance for a fresh start, not just every morning.',
    'Treat your evening like it matters. It does.',
    'You are building something that lasts longer than 45 days.',
    'Sleep, food, movement, calm. Small daily choices add up to how you feel.',
    'Be proud of the quiet effort no one else sees.'
  ];

  // Checkpoints: short-term wins on the way to the long-term goal.
  // "happening" = what the routine is doing (process, not promised feelings).
  // "look" = things to notice, phrased as invitations, per goal. Real progress = their own numbers.
  var CHECKPOINTS = {
    1: { title: 'Day 1: you started', happening: 'Today you set your starting point. Every score from now on is compared to this one, so you will see your own progress, not a promise.' },
    3: { title: 'Day 3: the routine is forming', happening: 'Three days of a daily capsule and check-ins. Your body is getting a steady daily supply of magnesium, and your brain is learning a new routine.',
      look: {
        sleep: ['Is your wind-down a little easier than on Day 1?', 'Did you keep the same wake-up time?'],
        stress: ['Do your shoulders feel a bit looser by evening?', 'Did you take a pause before reacting today?'],
        energy: ['How is your energy at 3 PM compared to Day 1?', 'Did you skip a late coffee?'],
        recovery: ['How do your muscles feel the morning after training?', 'Did you drink enough water after your workout?']
      } },
    7: { title: 'One week in', happening: 'A full week of steady magnesium and small habits. Magnesium builds up slowly in muscles and bones, so this is the foundation for the weeks ahead.',
      look: {
        sleep: ['Falling asleep with less tossing and turning', 'Waking up a little less groggy'],
        stress: ['Evenings that feel a bit calmer', 'Less tension in your jaw and shoulders'],
        energy: ['A smaller afternoon slump', 'Mornings that start a bit easier'],
        recovery: ['Less stiffness the day after training', 'Muscles that relax faster after effort']
      } },
    14: { title: 'Two weeks in', happening: 'Two weeks of consistency. Your routine is no longer new, and your habits are stacking on top of each other.',
      look: {
        sleep: ['Nights with fewer wake-ups', 'A bedtime routine you do without thinking'],
        stress: ['Bouncing back faster after a stressful moment', 'Feeling less "wired" at night'],
        energy: ['Steadier energy from morning to evening', 'Needing less caffeine to get going'],
        recovery: ['Getting back to training feeling ready', 'Fewer days where everything feels tight']
      } },
    21: { title: 'Three weeks: it is sticking', happening: 'Three weeks is when many habits start to feel normal. You are past the hardest part of building a routine.',
      look: {
        sleep: ['More mornings where you feel rested', 'Your sleep score trending up on the chart'],
        stress: ['More calm days than tense ones on your chart', 'Handling busy days with less effort'],
        energy: ['More good-energy days than drained ones', 'Your energy line rising on the chart'],
        recovery: ['Your recovery feeling more predictable', 'Training more often with less soreness']
      } },
    30: { title: 'One month strong', happening: 'A month of daily magnesium and habits. Look at your chart: this is your own record of how you have been feeling.',
      look: {
        sleep: ['Compare this week to your first week', 'Notice which habit helped your nights the most'],
        stress: ['Compare this week to your first week', 'Notice which habit helped you stay calm the most'],
        energy: ['Compare this week to your first week', 'Notice which habit helped your energy the most'],
        recovery: ['Compare this week to your first week', 'Notice which habit helped your recovery the most']
      } },
    45: { title: 'Day 45: you made it', happening: 'You finished Start, Build and Keep. The first 45 days built the routine. What you do next decides if you keep it: your body still uses magnesium every day, and habits fade faster than they form.' }
  };
  var CP_DAYS = [1, 3, 7, 14, 21, 30, 45];
  var CP_SHORT = { 1: 'Day 1', 3: 'Routine forming', 7: 'One week', 14: 'Two weeks', 21: 'Three weeks', 30: 'One month', 45: 'Day 45' };

  ICONS.peak ='<path d="M2 20 9 8l4 6 3-4 6 10z"/><path d="M9 8l1.6 2.7L9 12l-1.4-1.6z" fill="#fff" opacity=".85"/>';
  ICONS.capsule ='<rect x="3" y="8" width="18" height="8" rx="4" transform="rotate(-35 12 12)" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8.6 9.6l4.6 6.6" transform="rotate(0)" stroke="currentColor" stroke-width="2"/>';
  ICONS.tummy = '<path d="M12 21c-4.5 0-8-3-8-7.5C4 8 8 4 12 4s8 4 8 9.5c0 4.5-3.5 7.5-8 7.5z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9 12c1 1 2 1 3 0s2-1 3 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>';

  // ---------- utils ----------
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function toStr(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function todayStr() { return toStr(new Date()); }
  function addDays(str, n) { var p = str.split('-'); var d = new Date(+p[0], p[1] - 1, +p[2]); d.setDate(d.getDate() + n); return toStr(d); }
  function diffDays(a, b) {
    var pa = a.split('-'), pb = b.split('-');
    return Math.round((Date.UTC(pb[0], pb[1] - 1, pb[2]) - Date.UTC(pa[0], pa[1] - 1, pa[2])) / 86400000);
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function icon(name, cls) {
    return '<svg class="' + (cls || 'fpr-ico') + '" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' + ICONS[name] + '</svg>';
  }
  function round1(n) { return Math.round(n * 10) / 10; }
  function fmtDelta(n) { var r = round1(n); return r === 0 ? '±0' : (r > 0 ? '+' : '−') + Math.abs(r).toFixed(1); }
  function dirClass(n) { var r = round1(n); return r > 0 ? 'fpr-is-up' : (r < 0 ? 'fpr-is-down' : 'fpr-is-flat'); }
  function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ('0' + b.toString(16)).slice(-2); }).join(''); }
  function focusKey(el) {
    var s = '';
    ['data-action', 'data-field', 'data-value', 'data-ob', 'data-metric', 'data-unlock-input', 'data-n'].forEach(function (a) {
      if (el.hasAttribute(a)) s += '[' + a + '="' + String(el.getAttribute(a)).replace(/"/g, '\\"') + '"]';
    });
    return s || null;
  }
  function chip(action, field, value, label, on) {
    return '<button type="button" class="fpr-chip' + (on ? ' is-on' : '') + '" aria-pressed="' + !!on + '" data-action="' + action + '" data-field="' + field + '" data-value="' + value + '">' + label + '</button>';
  }
  function capsTaken(c) { return c.caps === true ? 2 : (+c.caps || 0); }
  function reducedMotion() { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } }
  // Vibrate only after a real tap (browsers block it otherwise and log an error).
  function haptic(ms) {
    try {
      var ua = navigator.userActivation;
      if (navigator.vibrate && (!ua || ua.hasBeenActive)) navigator.vibrate(ms || 12);
    } catch (e) {}
  }

  function App(root) {
    this.root = root;
    this.unlockHash = (root.getAttribute('data-unlock-hash') || '').trim().toLowerCase();
    this.productUrl = root.getAttribute('data-product-url') || '/products/full-peak-magnesium-complex';
    this.contactUrl = root.getAttribute('data-contact-url') || '/pages/contact';
    this.debug = root.getAttribute('data-debug') === 'true';
    this.form = document.querySelector('form[data-fpr-signup]');
    // Logged-in customer (private page). Progress is stored per customer on this device.
    this.customer = {
      id: root.getAttribute('data-customer-id') || '',
      email: root.getAttribute('data-customer-email') || '',
      name: root.getAttribute('data-customer-name') || '',
      marketing: root.getAttribute('data-customer-marketing') === 'true',
      bottles: +(root.getAttribute('data-bottles-owned') || 0)
    };
    this.key = KEY + (this.customer.id ? '-' + this.customer.id : '');
    // Store settings (theme editor > My Daily Peak section).
    this.capsPerBottle = +(root.getAttribute('data-caps-per-bottle') || CAPS_PER_BOTTLE) || CAPS_PER_BOTTLE;
    this.phase4Bottles = +(root.getAttribute('data-phase4-bottles') || 2) || 2;
    this.storageOk = true;
    this.migrateAnonymous();
    this.state = this.load();
    // Bought 2+ bottles (read from their orders by Liquid): Phase 4 opens by itself, no code needed.
    if (this.state && !this.state.unlocked && this.customer.bottles >= this.phase4Bottles) { this.state.unlocked = true; this.save(); }
    this.ob = null;           // onboarding draft
    this.ci = null;           // check-in draft
    this.ciDay = null;        // set when logging yesterday
    this.editing = false;
    this.flash = '';
    this.unlockError = '';
    this.unlockDraft = '';
    this.ignorePop = false;
    this.renderDay = null;
    this.viewKey = '';
    this.lastTags = '';
    var self = this;
    root.addEventListener('click', function (e) { self.onClick(e); });
    root.addEventListener('input', function (e) { self.onInput(e); });
    root.addEventListener('change', function (e) { self.onInput(e); });
    root.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.hasAttribute('data-unlock-input')) {
        e.preventDefault();
        var b = e.target.closest('.fpr-unlock').querySelector('[data-action="unlock"]');
        if (b) b.click();
      }
    });
    // Phone "back" during onboarding goes to the previous step instead of leaving the page.
    window.addEventListener('popstate', function () {
      if (self.ignorePop) { self.ignorePop = false; return; }
      if (!self.ob) return;
      if (self.ob.step > 0) {
        self.ob.step--;
        try { history.pushState({ fpr: 1 }, ''); } catch (e) {}
      } else {
        self.ob = null;
      }
      self.render('.fpr-h2, .fpr-h1');
    });
    // Page left open overnight: refresh to the new day when the visitor comes back.
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState !== 'visible' || !self.state || !self.state.start) return;
      if (self.day() !== self.renderDay) { self.resetDraft(); self.render(); }
    });
    // Same page open in another tab: pick up its changes instead of overwriting them.
    window.addEventListener('storage', function (e) {
      if (e.key !== self.key) return;
      self.state = self.load();
      self.resetDraft();
      self.render();
    });
    if (this.state) this.syncMilestones();
    this.render();
  }

  // Someone who started before logging in keeps their progress once they log in on the same device.
  App.prototype.migrateAnonymous = function () {
    if (!this.customer.id) return;
    try {
      var ls = window.localStorage;
      if (!ls.getItem(this.key) && ls.getItem(KEY)) { ls.setItem(this.key, ls.getItem(KEY)); ls.removeItem(KEY); }
    } catch (e) {}
  };

  App.prototype.load = function () {
    try {
      var raw = window.localStorage.getItem(this.key);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || s.v !== 1) return null;
      s.bottles = s.bottles || 1;
      s.capsPerDay = s.capsPerDay || 1;
      s.tips = s.tips || {};
      return s;
    } catch (e) {
      this.storageOk = false;
      return null;
    }
  };

  App.prototype.save = function () {
    try {
      window.localStorage.setItem(this.key, JSON.stringify(this.state));
      this.storageOk = true;
    } catch (e) {
      this.storageOk = false;
    }
  };

  App.prototype.resetDraft = function () {
    this.ci = null; this.ciDay = null; this.editing = false; this.flash = ''; this.dip = false;
  };

  // ---------- program logic ----------
  App.prototype.day = function () { return this.state && this.state.start ? diffDays(this.state.start, todayStr()) + 1 : 0; };
  App.prototype.limit = function () { return this.state.unlocked ? MAX_DAYS : CORE_DAYS; };
  App.prototype.phase = function (d) {
    for (var i = 0; i < PHASES.length; i++) if (d >= PHASES[i].from && d <= PHASES[i].to) return PHASES[i];
    return PHASES[PHASES.length - 1];
  };
  App.prototype.habit = function (d) {
    if (d === 1) return 'Take your capsule with ' + this.mealLabel() + " today. That's the whole job for Day 1.";
    if (d === 2 && this.state.capsPerDay === 2) return 'Taking a second capsule? Space it out from the first, never both at once.';
    if (d > CORE_DAYS) return MAINTAIN[(d - CORE_DAYS - 1) % MAINTAIN.length];
    var p = this.phase(d);
    var pool = HABITS[this.state.goal][p.id - 1];
    return pool[(d - p.from) % pool.length];
  };
  App.prototype.mealLabel = function () {
    var m = this.state && this.state.meal;
    return m ? m : 'a meal';
  };

  App.prototype.days = function () {
    return Object.keys(this.state.checkins).map(Number).sort(function (a, b) { return a - b; });
  };
  // Gentle streak: one missed day per 7 is forgiven, so a single slip doesn't wipe weeks of work.
  App.prototype.streak = function () {
    var c = this.state.checkins, d = this.day();
    if (!c[d]) d--;
    var n = 0, lastMiss = null;
    while (d >= 1) {
      if (c[d]) { n++; d--; continue; }
      if (n > 0 && c[d - 1] && (lastMiss === null || lastMiss - d >= 7)) { lastMiss = d; d--; continue; }
      break;
    }
    return n;
  };
  App.prototype.lastCheckinDay = function () {
    var days = this.days().filter(function (x) { return x < this.day(); }, this);
    return days.length ? days[days.length - 1] : 0;
  };
  // Back after 3+ days away (and not checked in yet today).
  App.prototype.isComeback = function () {
    var d = this.day(), last = this.lastCheckinDay();
    return !!last && !this.state.checkins[d] && d - last > 3;
  };
  App.prototype.avg = function (c) { return (c.sleep + c.calm + c.energy) / 3; };
  App.prototype.weekStats = function (from, to) {
    var st = this.state, n = 0, sums = { sleep: 0, calm: 0, energy: 0 }, habits = 0, best = null;
    for (var i = from; i <= to; i++) {
      if (st.habits[i]) habits++;
      var c = st.checkins[i];
      if (!c) continue;
      n++;
      METRICS.forEach(function (m) { sums[m.id] += c[m.id]; });
      if (!best || this.avg(c) > this.avg(st.checkins[best])) best = i;
    }
    var out = { n: n, habits: habits, best: best };
    METRICS.forEach(function (m) { out[m.id] = n ? sums[m.id] / n : null; });
    return out;
  };
  App.prototype.lastBefore = function (d) {
    var days = this.days().filter(function (x) { return x < d; });
    return days.length ? this.state.checkins[days[days.length - 1]] : null;
  };
  App.prototype.deltas = function () {
    var days = this.days();
    if (days.length < 2) return null;
    var base = this.state.checkins[days[0]];
    var recent = days.slice(-3).map(function (d) { return this.state.checkins[d]; }, this);
    var out = { from: days[0] };
    METRICS.forEach(function (m) {
      var avg = recent.reduce(function (s, c) { return s + c[m.id]; }, 0) / recent.length;
      out[m.id] = { base: base[m.id], now: avg, diff: avg - base[m.id] };
    });
    return out;
  };
  // ---------- short-term wins ----------
  // The personal win for a given check-in, built only from the person's own data.
  App.prototype.winFor = function (d) {
    var st = this.state, c = st.checkins[d];
    if (!c) return '';
    var prev = this.days().filter(function (x) { return x < d; });
    if (!prev.length) return 'Starting point set. Your plan has begun.';
    var best = null;
    METRICS.forEach(function (m) {
      var top = Math.max.apply(null, prev.map(function (x) { return st.checkins[x][m.id]; }));
      if (c[m.id] > top && (!best || c[m.id] > best.v)) best = { m: m, v: c[m.id] };
    });
    if (best) return 'New personal best: ' + best.m.label.toLowerCase() + ' ' + best.v + '/10.';
    var run = 0;
    for (var i = d; i >= 1 && st.checkins[i]; i--) run++;
    if ([3, 5, 7, 10, 14, 21, 30, 45, 60, 90].indexOf(run) >= 0) return run + ' check-ins in a row. That is a real routine.';
    var last = st.checkins[prev[prev.length - 1]], up = null;
    METRICS.forEach(function (m) { var df = c[m.id] - last[m.id]; if (df >= 1 && (!up || df > up.df)) up = { m: m, df: df }; });
    if (up) return up.m.label + ' is up ' + up.df + ' from your last check-in.';
    var base = st.checkins[prev[0]];
    if (METRICS.every(function (m) { return c[m.id] > base[m.id]; })) return 'All three scores are above your Day ' + prev[0] + '.';
    var caps = 0;
    for (var j = d; j >= 1 && st.checkins[j] && capsTaken(st.checkins[j]) > 0; j--) caps++;
    if (caps >= 3) return 'Capsule taken ' + caps + ' days in a row.';
    return 'You showed up today. That is how a routine is built.';
  };

  // The 3 daily steps. Finishing all three closes the day with a small reward.
  App.prototype.todaySteps = function (d) {
    var st = this.state, c = st.checkins[d];
    return [
      { label: 'Capsule', done: !!(c && capsTaken(c) > 0) },
      { label: 'Check-in', done: !!c },
      { label: 'Habit', done: !!st.habits[d] }
    ];
  };
  App.prototype.closeDay = function (d) {
    var st = this.state;
    st.complete = st.complete || {};
    if (st.complete[d] || !this.todaySteps(d).every(function (s) { return s.done; })) return '';
    st.complete[d] = true;
    this.save();
    return 'Day ' + d + ' complete. See you tomorrow!';
  };

  App.prototype.nextCheckpoint = function (d) {
    for (var i = 0; i < CP_DAYS.length; i++) if (CP_DAYS[i] > d) return CP_DAYS[i];
    return null;
  };

  // "You've built X": what they would put at risk, from their own data.
  App.prototype.builtSoFar = function () {
    var n = this.days().length, dl = this.deltas(), best = null;
    if (!n) return '';
    if (dl) METRICS.forEach(function (m) { if (dl[m.id].diff >= 0.5 && (!best || dl[m.id].diff > best.diff)) best = { m: m, diff: dl[m.id].diff }; });
    return 'You have checked in ' + n + ' time' + (n === 1 ? '' : 's') +
      (best ? ' and your ' + best.m.label.toLowerCase() + ' score is up ' + round1(best.diff).toFixed(1) + ' since Day ' + dl.from : '') + '. ';
  };

  App.prototype.supplyDays = function () { return Math.floor(this.state.bottles * this.capsPerBottle / this.state.capsPerDay); };

  App.prototype.verifyCode = function (code) {
    var hash = this.unlockHash;
    if (!code || !hash || !(window.crypto && window.crypto.subtle && window.TextEncoder)) return Promise.resolve(false);
    return window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(code))
      .then(function (b) { return hex(b) === hash; }, function () { return false; });
  };

  // ---------- Shopify customer tags ----------
  App.prototype.sendTags = function (tags) {
    var st = this.state, key = this.key;
    if (!st || !st.consent || !st.email) return;
    var fresh = tags.filter(function (t) { return !st.sent[t]; });
    if (!fresh.length) return;
    this.lastTags = fresh.join(', ');
    if (!this.form) {
      if (window.console) console.info('[My Daily Peak] preview mode, tags not sent:', this.lastTags);
      return;
    }
    fresh.forEach(function (t) { st.sent[t] = true; });
    this.save();
    var fd = new FormData(this.form);
    fd.set('contact[email]', st.email);
    fd.set('contact[tags]', fresh.join(','));
    if (st.name) fd.set('contact[first_name]', st.name);
    fetch(this.form.action, { method: 'POST', body: fd, credentials: 'same-origin' })
      .then(function (r) {
        // Shopify can answer with a bot challenge: in that case allow a retry on next visit.
        if (!r.ok || /challenge/.test(r.url)) throw new Error('not accepted');
      })
      .catch(function () {
        fresh.forEach(function (t) { delete st.sent[t]; });
        try { window.localStorage.setItem(key, JSON.stringify(st)); } catch (e) {}
      });
  };

  App.prototype.syncMilestones = function () {
    var d = this.day(), tags = [];
    if (!d) return;
    tags.push('fp-reset-started');
    [7, 21, 45, 90].forEach(function (m) { if (d >= m) tags.push('fp-reset-day' + m); });
    if (this.state.unlocked) tags.push('fp-reset-phase2');
    this.sendTags(tags);
  };

  // ---------- feedback: a short confirmation toast ----------
  App.prototype.celebrate = function (msg) {
    haptic(12);
    if (msg) this.toast(msg);
  };

  App.prototype.toast = function (msg) {
    var old = document.querySelector('.fpr-toast');
    if (old) old.remove();
    var t = document.createElement('div');
    t.className = 'fpr-toast';
    t.setAttribute('role', 'status');
    t.innerHTML = '<span class="fpr-toast-ico">' + icon('check') + '</span><span>' + esc(msg) + '</span>';
    document.body.appendChild(t);
    requestAnimationFrame(function () { t.classList.add('is-in'); });
    setTimeout(function () { t.classList.remove('is-in'); setTimeout(function () { t.remove(); }, 400); }, 2400);
  };

  // ---------- events ----------
  App.prototype.onClick = function (e) {
    var t = e.target.closest('[data-action]');
    if (!t || !this.root.contains(t)) return;
    var a = t.getAttribute('data-action');
    var st = this.state;
    var self = this;
    var focus = null;

    if (a === 'start') {
      var cu = this.customer;
      this.ob = {
        step: 0, extras: [],
        // Logged-in customers: prefill what Shopify already knows.
        name: cu.name, email: cu.email, consent: cu.marketing,
        bottles: cu.bottles >= 4 ? '4' : (cu.bottles >= 2 ? '2' : (cu.bottles === 1 ? '1' : undefined))
      };
      try { history.pushState({ fpr: 1 }, ''); } catch (err) {}
      focus = '.fpr-h2';
    }
    else if (a === 'pick') {
      this.ob[t.getAttribute('data-field')] = t.getAttribute('data-value');
      if (this.ob.sex === 'm' && this.ob.extras) this.ob.extras = this.ob.extras.filter(function (x) { return x !== 'peri'; });
      haptic(8);
    }
    else if (a === 'why-ex') { this.ob.why = t.getAttribute('data-value'); haptic(8); }
    else if (a === 'toggle-extra') {
      var ex = t.getAttribute('data-value'), list = this.ob.extras || (this.ob.extras = []);
      var at = list.indexOf(ex);
      if (at >= 0) list.splice(at, 1); else list.push(ex);
      haptic(8);
    }
    else if (a === 'next') { this.ob.step++; focus = '.fpr-h2'; }
    else if (a === 'back') {
      if (this.ob.step > 0) { this.ob.step--; focus = '.fpr-h2'; }
      else { this.ob = null; this.ignorePop = true; try { history.back(); } catch (err) { this.ignorePop = false; } focus = '.fpr-h1'; }
    }
    else if (a === 'finish') {
      if (!this.finishOnboarding()) return;
      this.ready = true;
      this.ignorePop = true;
      try { history.back(); } catch (err) { this.ignorePop = false; }
      focus = '.fpr-h1';
    }
    else if (a === 'go') {
      this.ready = false;
      this.render('.fpr-h1');
      var top0 = this.root.getBoundingClientRect().top + window.pageYOffset - 80;
      if (window.pageYOffset > top0) window.scrollTo(0, top0);
      if (st.start) this.celebrate('Day 1. Your plan starts now.');
      return;
    }
    else if (a === 'begin') {
      st.start = todayStr();
      this.save();
      this.syncMilestones();
      this.flash = '';
      this.render('.fpr-h1');
      this.celebrate('Day 1. Your plan starts now.');
      return;
    }
    else if (a === 'habit') {
      var hd = this.day();
      var nowDone = !st.habits[hd];
      if (nowDone) st.habits[hd] = true; else delete st.habits[hd];
      this.save();
      var closedH = nowDone ? this.closeDay(hd) : '';
      this.render();
      if (nowDone) this.celebrate(closedH || 'Habit done. Nice one.');
      return;
    }
    else if (a === 'cap') { var ci0 = +t.getAttribute('data-value'); this.ci.caps[ci0] = !this.ci.caps[ci0]; haptic(8); }
    else if (a === 'gut') { this.ci.gut = !this.ci.gut; haptic(8); }
    else if (a === 'save-checkin') {
      var target = this.ciDay || this.renderDay;
      var first = !this.days().length;
      st.checkins[target] = {
        sleep: +this.ci.sleep, calm: +this.ci.calm, energy: +this.ci.energy,
        caps: this.ci.caps.filter(Boolean).length, gut: !!this.ci.gut
      };
      this.save();
      var wasYesterday = !!this.ciDay;
      this.resetDraft();
      // A rough day (well below the last few) is when their "why" helps most.
      var prevDays = this.days().filter(function (x) { return x < target; }).slice(-3);
      if (prevDays.length >= 2) {
        var prevAvg = prevDays.reduce(function (s, x) { return s + self.avg(st.checkins[x]); }, 0) / prevDays.length;
        this.dip = this.avg(st.checkins[target]) <= prevAvg - 1.5;
      } else this.dip = false;
      var count = this.days().length, badge = null;
      BADGES.forEach(function (b) { if (b.n === count) badge = b; });
      var msg;
      var closed = wasYesterday ? '' : this.closeDay(target);
      if (badge) msg = 'Milestone unlocked: ' + badge.name + '!';
      else if (closed) msg = closed;
      else if (wasYesterday) msg = 'Day ' + target + ' added.';
      else msg = this.winFor(target);
      this.render('.fpr-checkin .fpr-h3');
      this.celebrate(msg);
      return;
    }
    else if (a === 'log-yesterday') { this.ciDay = this.day() - 1; this.ci = null; this.editing = true; this.flash = ''; focus = '.fpr-checkin .fpr-h3'; }
    else if (a === 'cancel-checkin') { this.resetDraft(); }
    else if (a === 'edit-checkin') { this.editing = true; this.ci = null; this.ciDay = null; this.flash = ''; focus = '.fpr-checkin .fpr-h3'; }
    else if (a === 'unlock') {
      var input = t.closest('.fpr-unlock').querySelector('[data-unlock-input]');
      var code = input ? input.value.trim().toUpperCase() : '';
      this.unlockDraft = input ? input.value : '';
      t.disabled = true;
      this.verifyCode(code).then(function (ok) {
        if (ok) {
          self.state.unlocked = true;
          self.unlockError = '';
          self.unlockDraft = '';
          self.save();
          self.sendTags(['fp-reset-phase2']);
          self.flash = '';
          self.render('.fpr-h1');
          self.celebrate('Phase 4 unlocked!', self.root.querySelector('.fpr-head'));
        } else {
          self.unlockError = code ? "That code doesn't match. Check your order confirmation email, or contact us and we'll send it again." : 'Enter the code from your order confirmation email.';
          haptic([10, 50, 10]);
          self.render('[data-unlock-input]');
        }
      });
      return;
    }
    else if (a === 'set') {
      var f = t.getAttribute('data-field'), v = t.getAttribute('data-value');
      st[f] = (f === 'bottles' || f === 'capsPerDay') ? +v : v;
      if (f === 'capsPerDay') this.ci = null;
      this.save();
      haptic(8);
    }
    else if (a === 'dismiss-tip') { st.tips[t.getAttribute('data-value')] = this.day() || true; this.save(); focus = '.fpr-h1'; }
    else if (a === 'restart') {
      if (!window.confirm('Start over? This clears your check-ins on this device.')) return;
      try { window.localStorage.removeItem(this.key); } catch (err) {}
      this.state = null; this.ob = null; this.resetDraft();
      focus = '.fpr-h1';
    }
    // debug helpers (day simulator)
    else if (a === 'dbg-shift') {
      if (!st.start) return;
      var ns = addDays(st.start, -(+t.getAttribute('data-n')));
      if (diffDays(ns, todayStr()) < 0) return;
      st.start = ns; this.save(); this.resetDraft(); this.syncMilestones();
    }
    else if (a === 'dbg-fill') { this.fillDemo(); }
    else return;

    this.render(focus);
    if (focus && (a === 'start' || a === 'next' || a === 'back' || a === 'finish' || a === 'restart')) {
      var top = this.root.getBoundingClientRect().top + window.pageYOffset - 80;
      if (window.pageYOffset > top) window.scrollTo(0, top);
    }
  };

  App.prototype.onInput = function (e) {
    var t = e.target;
    var f = t.getAttribute('data-ob');
    if (f && this.ob) {
      this.ob[f] = t.type === 'checkbox' ? t.checked : t.value;
      var btn = this.root.querySelector('[data-action="finish"]');
      if (btn) btn.disabled = !this.canFinish();
      var hint = this.root.querySelector('[data-email-hint]');
      if (hint) { var msg = this.emailHint(); hint.textContent = msg; hint.hidden = !msg; }
      var fields = this.root.querySelector('[data-remind-fields]');
      if (fields) fields.hidden = !this.ob.consent;
      if (f === 'why') [].forEach.call(this.root.querySelectorAll('[data-action="why-ex"]'), function (b) { b.classList.toggle('is-on', b.getAttribute('data-value') === t.value); });
      return;
    }
    if (t.hasAttribute('data-unlock-input')) { this.unlockDraft = t.value; return; }
    if (t.hasAttribute('data-why') && this.state) { this.state.why = t.value.slice(0, 140); this.save(); return; }
    var m = t.getAttribute('data-metric');
    if (m && this.ci) {
      if (this.ci[m] !== +t.value && e.type === 'input') haptic(4);
      this.ci[m] = +t.value;
      var out = this.root.querySelector('[data-out="' + m + '"]');
      if (out) out.textContent = t.value;
      t.style.setProperty('--fpr-fill', ((t.value - 1) / 9 * 100) + '%');
    }
  };

  App.prototype.emailValid = function () { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test((this.ob.email || '').trim()); };
  App.prototype.canFinish = function () { return !this.ob.consent || !!this.customer.email || this.emailValid(); };
  App.prototype.emailHint = function () {
    if (this.customer.email) return '';
    return this.ob.consent && !this.emailValid() ? 'Add a valid email to get the reminder.' : '';
  };

  App.prototype.finishOnboarding = function () {
    var ob = this.ob;
    if (!this.canFinish()) return false;
    var consent = !!this.customer.email || !!ob.consent;
    var wait = ob.start === 'wait';
    this.state = {
      v: 1,
      created: todayStr(),
      start: wait ? null : addDays(todayStr(), -(+ob.start || 0)),
      goal: ob.goal,
      bottles: +ob.bottles || this.customer.bottles || 1,
      capsPerDay: +ob.capsPerDay || 1,
      meal: ob.meal || 'dinner',
      profile: { age: ob.age, sex: ob.sex, feel: ob.feel, tried: ob.tried, extras: (ob.extras || []).slice() },
      name: (ob.name || '').trim().slice(0, 40),
      why: (ob.why || '').trim().slice(0, 140),
      email: consent ? (this.customer.email || (ob.email || '').trim()) : '',
      consent: consent,
      checkins: {},
      habits: {},
      unlocked: this.customer.bottles >= this.phase4Bottles,
      tips: {},
      sent: {}
    };
    this.ob = null;
    this.save();
    this.sendTags([
      'fp-reset',
      'fp-goal-' + ob.goal,
      'fp-age-' + ob.age,
      'fp-sex-' + ob.sex,
      'fp-feel-' + ob.feel,
      'fp-tried-' + ob.tried,
      'fp-meal-' + ob.meal,
      'fp-bottles-' + this.state.bottles,
      'fp-caps-' + this.state.capsPerDay
    ].concat((ob.extras || []).map(function (x) { return 'fp-extra-' + x; })));
    this.syncMilestones();
    return true;
  };

  App.prototype.fillDemo = function () {
    var st = this.state, d = this.day();
    for (var i = 1; i < d; i++) {
      if (st.checkins[i] || Math.random() < 0.12) continue; // keep real entries, skip a few days like real life
      var lift = Math.min(i / 30, 1) * 3.5;
      var r = function () { return Math.round(Math.random() * 2 - 1); };
      st.checkins[i] = {
        sleep: Math.max(1, Math.min(10, Math.round(4 + lift + r()))),
        calm: Math.max(1, Math.min(10, Math.round(4 + lift * 0.9 + r()))),
        energy: Math.max(1, Math.min(10, Math.round(5 + lift * 0.7 + r()))),
        caps: Math.random() > 0.1 ? st.capsPerDay : 0,
        gut: false
      };
      if (Math.random() > 0.3) st.habits[i] = true;
    }
    this.save();
  };

  // ---------- views ----------
  App.prototype.currentViewKey = function () {
    if (this.ob) return 'ob' + this.ob.step;
    if (this.ready) return 'ready';
    if (!this.state) return 'welcome';
    if (!this.state.start) return 'wait';
    return 'dash' + this.day();
  };

  App.prototype.render = function (focusSel) {
    var key = null, ae = document.activeElement;
    if (!focusSel && ae && ae !== this.root && this.root.contains(ae)) key = focusKey(ae);

    var html;
    if (this.ob) html = this.viewOnboarding();
    else if (!this.state) html = this.viewWelcome();
    else if (this.ready) html = this.viewReady();
    else if (!this.state.start) html = this.viewWaiting();
    else html = this.viewDashboard();
    if (!this.storageOk) html = '<p class="fpr-note">Your browser is not saving progress (private mode?). Open this page in a normal window to keep your check-ins.</p>' + html;
    if (this.debug) html = this.viewDebug() + html;

    // Entrance animation only when the screen changes, never on in-place updates.
    var vk = this.currentViewKey();
    var entering = vk !== this.viewKey;
    this.viewKey = vk;
    this.root.innerHTML = html;
    this.renderDay = this.state && this.state.start ? this.day() : null;
    var kids = this.root.children;
    for (var i = 0; i < kids.length; i++) kids[i].style.setProperty('--i', i);
    if (entering && !reducedMotion()) {
      var root = this.root;
      root.classList.remove('fpr-enter');
      void root.offsetWidth;
      root.classList.add('fpr-enter');
      clearTimeout(this.enterTimer);
      this.enterTimer = setTimeout(function () { root.classList.remove('fpr-enter'); }, 1200);
    }
    // Paint slider fills.
    var ranges = this.root.querySelectorAll('input[type=range]');
    for (var r = 0; r < ranges.length; r++) ranges[r].style.setProperty('--fpr-fill', ((ranges[r].value - 1) / 9 * 100) + '%');

    var target = focusSel ? this.root.querySelector(focusSel) : (key ? this.root.querySelector(key) : null);
    if (target) {
      if (focusSel && !target.matches('button, input, a')) target.setAttribute('tabindex', '-1');
      try { target.focus({ preventScroll: true }); } catch (e) { target.focus(); }
    }
  };

  // Brand lockup: peak mark + "My Daily Peak".
  function logo(cls) {
    return '<div class="fpr-logo ' + (cls || '') + '" aria-label="My Daily Peak">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M1.5 21 9 8.5l4.2 7 2.6-4.2L22.5 21z" fill="currentColor"/><circle cx="18.5" cy="5" r="2.2" fill="currentColor"/></svg>' +
      '<span>My Daily <strong>Peak</strong></span></div>';
  }

  App.prototype.viewWelcome = function () {
    return '' +
      '<section class="fpr-hero">' +
        logo('fpr-logo-lg') +
        '<span class="fpr-eyebrow">Included with PeakMag</span>' +
        '<h1 class="fpr-h1">Your personal daily plan</h1>' +
        '<p class="fpr-lead">Your capsule does its part. This is the other part: a plan built around your goal, a 10-second check-in, one small habit a day, and a clear view of how far you\'ve come.</p>' +
        '<ul class="fpr-points">' +
          '<li>' + icon('check') + 'Built around your goal and your routine</li>' +
          '<li>' + icon('check') + 'Small wins every day, checkpoints every week</li>' +
          '<li>' + icon('check') + 'Your Day 1 vs today, on one chart</li>' +
        '</ul>' +
        '<button type="button" class="fpr-btn" data-action="start">Build my plan</button>' +
        '<p class="fpr-fine">Takes 60 seconds. Nothing to download.</p>' +
      '</section>' +
      this.viewJourney(0);
  };

  App.prototype.viewOnboarding = function () {
    var ob = this.ob, cu = this.customer, body = '', ready = false, s = ob.step, cta = null;
    var group = function (legend, field, opts, col, action) {
      return '<fieldset class="fpr-q"><legend>' + legend + '</legend><div class="fpr-chips' + (col ? ' fpr-chips-col' : '') + '">' +
        opts.map(function (o) { return chip(action || 'pick', field, o[0], o[1], ob[field] === o[0]); }).join('') + '</div></fieldset>';
    };

    if (s === 0) {
      // Customer: picks their plan. Us: the desire that brought them (ad angle).
      body = '<h2 class="fpr-h2">What do you want PeakMag to help with most?</h2>' +
        '<p class="fpr-sub">Pick one. Your daily plan is built around it.</p><div class="fpr-goals">' +
        Object.keys(GOALS).map(function (k) {
          var on = ob.goal === k;
          return '<button type="button" class="fpr-goal' + (on ? ' is-on' : '') + '" aria-pressed="' + on + '" data-action="pick" data-field="goal" data-value="' + k + '">' +
            icon(k, 'fpr-goal-ico') + '<span><strong>' + GOALS[k].label + '</strong><small>' + GOALS[k].sub + '</small></span></button>';
        }).join('') + '</div>';
      ready = !!ob.goal;
    } else if (s === 1) {
      // Customer: "this plan fits me". Us: the avatar (age, sex, how they feel, segments).
      var extras = EXTRAS.filter(function (o) { return !(o[0] === 'peri' && ob.sex === 'm'); });
      body = '<h2 class="fpr-h2">A little about you</h2><p class="fpr-sub">So your plan fits your life. About 10 seconds.</p>' +
        '<fieldset class="fpr-q"><legend>Your age</legend><div class="fpr-segbtns fpr-segbtns-4">' +
          AGES.map(function (o) { return chip('pick', 'age', o[0], o[1], ob.age === o[0]); }).join('') + '</div></fieldset>' +
        '<fieldset class="fpr-q"><legend>You are</legend><div class="fpr-segbtns fpr-segbtns-3">' +
          SEXES.map(function (o) { return chip('pick', 'sex', o[0], o[1], ob.sex === o[0]); }).join('') + '</div></fieldset>' +
        '<fieldset class="fpr-q"><legend>Most days, you feel…</legend><div class="fpr-feel">' +
          FEELS.map(function (o) {
            var on = ob.feel === o[0];
            return '<button type="button" class="fpr-feel-opt' + (on ? ' is-on' : '') + '" aria-pressed="' + on + '" data-action="pick" data-field="feel" data-value="' + o[0] + '">' +
              '<strong>' + o[1] + '</strong><small>' + o[2] + '</small></button>';
          }).join('') + '</div></fieldset>' +
        '<fieldset class="fpr-q"><legend>Anything else going on? <em>Optional, tap any</em></legend><div class="fpr-chips">' +
          extras.map(function (o) { return chip('toggle-extra', 'extras', o[0], o[1], (ob.extras || []).indexOf(o[0]) >= 0); }).join('') + '</div></fieldset>';
      ready = !!ob.age && !!ob.sex && !!ob.feel;
    } else if (s === 2) {
      // Customer: a routine they can't forget + tips that match their past. Us: objections and dosing behavior.
      body = '<h2 class="fpr-h2">Your capsule routine</h2><p class="fpr-sub">Tying your capsule to a meal you never skip is the easiest way to never forget it.</p>' +
        group('Have you taken magnesium before?', 'tried', TRIED, true) +
        group('How many capsules a day?', 'capsPerDay', CAPS) +
        '<p class="fpr-small fpr-q-note">Start with 1. If you add a 2nd, take it at a different meal, never both at once.</p>' +
        group(ob.capsPerDay === '2' ? 'Your first capsule goes with…' : 'Your capsule goes with…', 'meal', MEALS);
      ready = !!ob.tried && !!ob.capsPerDay && !!ob.meal;
    } else if (s === 3) {
      // Customer: refill reminders at the right time + Day 1 that starts when the bottle arrives.
      var knowBottles = cu.bottles > 0;
      body = '<h2 class="fpr-h2">Your bottles</h2><p class="fpr-sub">So Day 1 starts on the right day, and we remind you before you run out.</p>' +
        (knowBottles ? '<p class="fpr-known">' + icon('check', 'fpr-ico-sm') + ' We found ' + cu.bottles + ' bottle' + (cu.bottles === 1 ? '' : 's') + ' in your orders.</p>' : group('How many bottles did you order?', 'bottles', BOTTLES)) +
        group('When did you take your first capsule?', 'start', STARTS, true);
      ready = (knowBottles || !!ob.bottles) && !!ob.start;
    } else {
      // Customer: their own reason, shown back on hard days.
      var exs = WHY_EXAMPLES[ob.goal] || WHY_EXAMPLES.sleep;
      body = '<h2 class="fpr-h2">Why does this matter to you?</h2>' +
        '<p class="fpr-sub">On the hard days, we will show you your own words. Tap one or write your own.</p>' +
        '<div class="fpr-why-ex">' + exs.map(function (x) {
          return '<button type="button" class="fpr-chip' + (ob.why === x ? ' is-on' : '') + '" data-action="why-ex" data-value="' + esc(x) + '">' + esc(x) + '</button>';
        }).join('') + '</div>' +
        '<label class="fpr-field"><span class="fpr-sr">Your reason</span>' +
          '<textarea rows="2" maxlength="140" data-ob="why" placeholder="Or write your own…">' + esc(ob.why) + '</textarea></label>';
      // Tapping "Build my plan" saves the answers to the customer's profile (as tags). No marketing opt-in here.
      var logged = !!cu.email;
      cta = '<button type="button" class="fpr-btn" data-action="finish">Build my plan</button>' +
        (logged ? '<p class="fpr-consent-note">Your answers are saved to your PeakMag profile so we can keep improving your plan.</p>' : '');
    }
    return this.wrapStep(s, body, cta || '<button type="button" class="fpr-btn" data-action="next"' + (ready ? '' : ' disabled') + '>Continue</button>');
  };

  App.prototype.wrapStep = function (s, body, cta) {
    var dots = '';
    for (var i = 0; i < OB_STEPS; i++) dots += '<span class="' + (i <= s ? 'is-on' : '') + '"></span>';
    return '<section class="fpr-card fpr-ob">' +
      '<div class="fpr-ob-top"><button type="button" class="fpr-link" data-action="back">← Back</button><div class="fpr-dots" role="img" aria-label="Step ' + (s + 1) + ' of ' + OB_STEPS + '">' + dots + '</div></div>' +
      body + '<div class="fpr-ob-cta">' + cta + '</div></section>';
  };

  // "Your plan is ready": shows the customer how their answers shaped the plan (perceived value).
  var TRIED_LINE = {
    first: 'New to magnesium: we start gentle and explain everything as you go.',
    nowork: 'Did not notice much before? This time your plan tracks your scores, so you can see your own trend.',
    stomach: 'Sensitive stomach: one capsule with a meal, and we check in on it every day.'
  };
  App.prototype.viewReady = function () {
    var st = this.state, p = st.profile || {};
    var feel = FEELS.filter(function (o) { return o[0] === p.feel; })[0];
    var caps = st.capsPerDay === 2 ? '2 a day: one with ' + st.meal + ', one at another meal' : '1 a day, with ' + st.meal;
    var rows = [
      ['Your goal', GOALS[st.goal].label],
      ['Your capsule', caps],
      ['Your starting point', feel ? feel[1] : ''],
      ['First checkpoint', st.start ? 'Day 3' : 'Day 3, counting from when your bottle arrives']
    ].filter(function (r) { return r[1]; });
    return '<section class="fpr-head fpr-ready">' + logo() +
        '<span class="fpr-eyebrow">' + icon('check', 'fpr-ico-sm') + ' Built for you</span>' +
        '<h1 class="fpr-h1">' + (st.name ? esc(st.name) + ', your' : 'Your') + ' plan is ready</h1>' +
        '<ul class="fpr-ready-list">' + rows.map(function (r) { return '<li><span>' + r[0] + '</span><strong>' + esc(r[1]) + '</strong></li>'; }).join('') + '</ul>' +
        (p.tried && TRIED_LINE[p.tried] ? '<p class="fpr-ready-note">' + TRIED_LINE[p.tried] + '</p>' : '') +
        (st.why ? '<p class="fpr-ready-why">“' + esc(st.why) + '”</p>' : '') +
        '<button type="button" class="fpr-btn" data-action="go">' + (st.start ? 'Start Day 1' : 'Got it') + '</button>' +
      '</section>';
  };

  App.prototype.viewWaiting = function () {
    var st = this.state;
    return '' +
      '<section class="fpr-head">' +
        logo() +
        (st.name ? '<p class="fpr-hello">Hi ' + esc(st.name) + '</p>' : '') +
        '<span class="fpr-eyebrow">Your plan · ' + GOALS[st.goal].label + '</span>' +
        '<h1 class="fpr-h1">Your bottle is on its way</h1>' +
        '<p class="fpr-lead">Day 1 starts the day you take your first capsule, not before. Come back here when it arrives.</p>' +
      '</section>' +
      '<section class="fpr-card fpr-arrived">' +
        '<div class="fpr-card-top"><span class="fpr-eyebrow">' + icon('box', 'fpr-ico-sm') + ' Bottle arrived?</span></div>' +
        '<p class="fpr-sub">Take your first capsule with ' + this.mealLabel() + ', then tap below. You\'ll do your Day 1 check-in right away.</p>' +
        '<button type="button" class="fpr-btn" data-action="begin">I took my first capsule today</button>' +
      '</section>' +
      '<section class="fpr-card fpr-habit">' +
        '<div class="fpr-card-top"><span class="fpr-eyebrow">' + icon(st.goal, 'fpr-ico-sm') + ' While you wait</span></div>' +
        '<p class="fpr-habit-text">' + HABITS[st.goal][0][0] + '</p>' +
        '<p class="fpr-small">A head start for your first week.</p>' +
      '</section>' +
      this.viewJourney(0) + this.viewSettings() + this.viewFooter();
  };

  App.prototype.viewDashboard = function () {
    var st = this.state, d = this.day(), lim = this.limit();
    var shown = Math.min(d, lim);
    var p = this.phase(shown);
    var eyebrow, title;
    if (d > MAX_DAYS) { eyebrow = '90 days complete'; title = 'Day ' + d; }
    else if (d > CORE_DAYS && !st.unlocked) { eyebrow = 'Start, Build, Keep: done'; title = 'Day ' + d; }
    else { eyebrow = 'Phase ' + p.id + ' · ' + p.name; title = 'Day ' + d + ' <span>of ' + lim + '</span>'; }

    var steps = this.todaySteps(d), doneN = steps.filter(function (s) { return s.done; }).length;
    var next = this.nextCheckpoint(d);

    var html = '' +
      '<section class="fpr-head">' +
        logo() +
        (st.name ? '<p class="fpr-hello">Hi ' + esc(st.name) + '</p>' : '') +
        '<span class="fpr-eyebrow">' + eyebrow + '</span>' +
        '<h1 class="fpr-h1">' + title + '</h1>' +
        '<p class="fpr-quote">' + QUOTES[(d - 1) % QUOTES.length] + '</p>' +
        // Today's 3 steps: the smallest possible win loop.
        '<div class="fpr-today' + (doneN === 3 ? ' is-complete' : '') + '">' +
          '<div class="fpr-today-top"><span>' + (doneN === 3 ? 'Day ' + d + ' complete' : 'Today: ' + doneN + ' of 3 done') + '</span>' +
          (next ? '<span class="fpr-next">Next checkpoint: ' + CP_SHORT[next] + ' · ' + (next - d === 1 ? 'tomorrow' : 'in ' + (next - d) + ' days') + '</span>' : '') + '</div>' +
          '<ul>' + steps.map(function (s) {
            return '<li class="' + (s.done ? 'is-done' : '') + '"><span class="fpr-today-ico">' + icon('check') + '</span>' + s.label + '</li>';
          }).join('') + '</ul>' +
        '</div>' +
        this.viewProgressBar(shown, lim) +
        '<div class="fpr-stats">' +
          '<div><strong>' + this.streak() + '</strong><span>day streak</span></div>' +
          '<div><strong>' + this.days().length + '</strong><span>check-ins</span></div>' +
          '<div><strong>' + Object.keys(st.habits).length + '</strong><span>habits done</span></div>' +
        '</div>' +
      '</section>';

    html += this.viewComeback(d) + this.viewCheckpoint(d) + this.viewMilestone(d) + this.viewWeek(d) + this.viewCheckin(d) + this.viewWhy(d) + this.viewHabit(d) + this.viewInsight(d) + this.viewExtra(d) + this.viewNudges(d);
    html += this.viewProgress() + this.viewBadges() + this.viewJourney(d) + this.viewSettings() + this.viewFooter();
    return html;
  };

  // Checkpoint card: what you did (real data) + what the routine is doing + what to look for + next step.
  App.prototype.viewCheckpoint = function (d) {
    var cp = CHECKPOINTS[d];
    if (!cp) return '';
    var st = this.state, self = this;
    var capDays = this.days().filter(function (x) { return x <= d && capsTaken(st.checkins[x]) > 0; }).length;
    var habits = Object.keys(st.habits).filter(function (x) { return +x <= d; }).length;
    var dl = this.deltas();
    var look = cp.look && cp.look[st.goal];
    var next = this.nextCheckpoint(d);
    var html = '<section class="fpr-card fpr-checkpoint">' +
      '<span class="fpr-eyebrow">' + icon('peak', 'fpr-ico-sm') + ' Checkpoint · Day ' + d + '</span>' +
      '<h2 class="fpr-h2">' + cp.title + '</h2>';
    if (d > 1) {
      html += '<div class="fpr-cp-stats">' +
        '<div><strong>' + this.days().length + '</strong><span>check-ins</span></div>' +
        '<div><strong>' + capDays + '</strong><span>capsule days</span></div>' +
        '<div><strong>' + habits + '</strong><span>habits done</span></div></div>';
    }
    html += '<h3 class="fpr-cp-label">What is happening</h3><p>' + cp.happening + '</p>';
    if (look) {
      html += '<h3 class="fpr-cp-label">Things to look for</h3><ul class="fpr-cp-look">' +
        look.map(function (l) { return '<li>' + l + '</li>'; }).join('') + '</ul>' +
        '<p class="fpr-small">Everyone is different. Not there yet? That is normal, it builds. Your chart shows your real progress.</p>';
    }
    if (d > 1 && dl) {
      html += '<h3 class="fpr-cp-label">Your numbers since Day ' + dl.from + '</h3><div class="fpr-cp-deltas">' + METRICS.map(function (m) {
        return '<span class="fpr-m-' + m.id + '">' + m.label + ' <strong class="' + dirClass(dl[m.id].diff) + '">' + fmtDelta(dl[m.id].diff) + '</strong></span>';
      }).join('') + '</div>';
    }
    if (d === 1) {
      html += '<p class="fpr-small">Your first checkpoint is on Day 3. Do today\'s 3 steps: capsule, check-in, habit.</p>';
    } else if (next) {
      html += '<p class="fpr-cp-next">Next checkpoint: <strong>' + CP_SHORT[next] + '</strong> on Day ' + next + '</p>';
    }
    void self;
    return html + '</section>';
  };

  App.prototype.whyQuote = function () {
    return this.state.why ? '<blockquote class="fpr-why-text">“' + esc(this.state.why) + '”</blockquote>' : '';
  };

  App.prototype.viewComeback = function (d) {
    if (!this.isComeback()) return '';
    return '<section class="fpr-card fpr-comeback">' +
      '<span class="fpr-eyebrow">' + icon('peak', 'fpr-ico-sm') + ' Welcome back</span>' +
      '<h2 class="fpr-h3">Pick up where you left off</h2>' +
      '<p>A few days off doesn\'t undo your progress. It\'s all still here. Today\'s check-in is the next step up.</p>' +
      (this.state.why ? '<p class="fpr-small">You told us why you started:</p>' + this.whyQuote() : '') +
      '</section>';
  };

  // Shown right after a rough check-in, and as a reminder on days 14 and 30.
  App.prototype.viewWhy = function (d) {
    var st = this.state;
    if (!st.why || this.isComeback()) return '';
    var rough = this.dip && st.checkins[d];
    if (!rough && d !== 14 && d !== 30) return '';
    return '<section class="fpr-card fpr-why">' +
      '<span class="fpr-eyebrow">' + icon('peak', 'fpr-ico-sm') + (rough ? ' Rough day? That\'s part of the climb' : ' Remember why you started') + '</span>' +
      this.whyQuote() +
      '<p class="fpr-small">' + (rough ? 'One hard day doesn\'t change the trend. Look at your chart below.' : 'Keep going. This is what it\'s for.') + '</p></section>';
  };

  // Every 7 days: this week vs the week before.
  App.prototype.viewWeek = function (d) {
    if (d < 8 || (d - 1) % 7 !== 0) return '';
    var wk = (d - 1) / 7, cur = this.weekStats(d - 7, d - 1), prev = wk > 1 ? this.weekStats(d - 14, d - 8) : null;
    if (!cur.n) return '';
    var rows = METRICS.map(function (m) {
      var diff = prev && prev.n ? cur[m.id] - prev[m.id] : null;
      return '<div class="fpr-m-' + m.id + '"><span>' + m.label + '</span><strong>' + cur[m.id].toFixed(1) + '</strong>' +
        (diff != null ? '<em class="' + dirClass(diff) + '">' + fmtDelta(diff) + '</em>' : '') + '</div>';
    }).join('');
    return '<section class="fpr-card fpr-week">' +
      '<span class="fpr-eyebrow">' + icon('check', 'fpr-ico-sm') + ' Week ' + wk + ' recap</span>' +
      '<h2 class="fpr-h3">' + (cur.n >= 6 ? 'What a week.' : (cur.n >= 4 ? 'Solid week.' : 'Every week counts.')) + '</h2>' +
      '<div class="fpr-scores">' + rows + '</div>' +
      '<p class="fpr-small">' + cur.n + '/7 check-ins · ' + cur.habits + '/7 habits' + (cur.best ? ' · Best day: Day ' + cur.best : '') + (prev && prev.n ? ' · vs week ' + (wk - 1) : '') + '</p>' +
      '</section>';
  };

  // Order of the "Inside your capsule" cards for this person.
  App.prototype.formSeq = function () {
    var g = GOAL_QS[this.state.goal] || GOAL_QS.sleep;
    var seq = ['deficit', g[0], 'blood', g[1], 'meet8', this.state.capsPerDay === 2 ? 'when2' : 'when1', g[2],
      'stomach', 'coffee', g[3], 'oxide', 'whyours', g[4], 'howlong', 'daily', 'stop'];
    // Answer their own objection first (from "Have you taken magnesium before?").
    var first = { stomach: 'stomach', nowork: 'howlong' }[(this.state.profile || {}).tried];
    if (first) { seq.splice(seq.indexOf(first), 1); seq.unshift(first); }
    return seq;
  };

  // Days without a science card get one extra card. Within the 45 days, forms and thoughts alternate
  // (forms first, until all are told); after that, thoughts only. Deterministic, so a day always shows the same card.
  App.prototype.dailyExtra = function (d) {
    if (d < 2 || INSIGHTS[d]) return null;
    var seq = this.formSeq(), k = 0, f = 0, t = 0;
    for (var i = 2; i <= d; i++) {
      if (INSIGHTS[i]) continue;
      var item;
      if (i <= CORE_DAYS && k % 2 === 0 && f < seq.length) item = { type: 'form', key: seq[f++] };
      else item = { type: 'thought', idx: t++ };
      if (i <= CORE_DAYS) k++;
      if (i === d) return item;
    }
    return null;
  };

  App.prototype.viewExtra = function (d) {
    var it = this.dailyExtra(d);
    if (!it) return '';
    if (it.type === 'thought') {
      return '<section class="fpr-card fpr-thought">' +
        '<span class="fpr-eyebrow">' + icon('peak', 'fpr-ico-sm') + ' A thought for today</span>' +
        '<p class="fpr-thought-text">' + THOUGHTS[it.idx % THOUGHTS.length] + '</p></section>';
    }
    var data = ANSWERS[it.key];
    return '<section class="fpr-card fpr-form">' +
      '<span class="fpr-eyebrow">' + icon('capsule', 'fpr-ico-sm') + ' Magnesium, answered</span>' +
      '<h2 class="fpr-h3">' + data[0] + '</h2><p>' + data[1] + '</p></section>';
  };

  App.prototype.viewInsight = function (d) {
    var it = INSIGHTS[d];
    if (!it) return '';
    return '<section class="fpr-card fpr-insight">' +
      '<span class="fpr-eyebrow">' + icon('sleep', 'fpr-ico-sm') + ' Science, simply</span>' +
      '<h2 class="fpr-h3">' + it[0] + '</h2><p>' + it[1] + '</p></section>';
  };

  App.prototype.viewBadges = function () {
    var count = this.days().length;
    if (!count) return '';
    var next = null;
    BADGES.forEach(function (b) { if (!next && b.n > count) next = b; });
    return '<section class="fpr-card"><h2 class="fpr-h3">Your milestones</h2>' +
      '<p class="fpr-sub">' + (next ? (next.n - count) + ' more check-in' + (next.n - count === 1 ? '' : 's') + ' to <strong>' + next.name + '</strong>.' : 'You reached the summit. Every milestone is yours.') + '</p>' +
      '<ul class="fpr-badges">' + BADGES.map(function (b) {
        var got = count >= b.n;
        return '<li class="' + (got ? 'is-got' : '') + '"><span class="fpr-badge-ico">' + icon(got ? 'peak' : 'lock') + '</span><strong>' + b.name + '</strong><small>' + b.n + ' check-ins</small></li>';
      }).join('') + '</ul></section>';
  };

  App.prototype.viewProgressBar = function (d, lim) {
    var segs = PHASES.filter(function (p) { return p.from <= lim; }).map(function (p) {
      var to = Math.min(p.to, lim);
      var len = to - p.from + 1;
      var fill = Math.max(0, Math.min(len, d - p.from + 1)) / len * 100;
      return '<div class="fpr-seg" style="flex:' + len + '"><i style="width:' + fill + '%"></i></div>';
    }).join('');
    return '<div class="fpr-bar" role="progressbar" aria-label="Program progress" aria-valuemin="1" aria-valuemax="' + lim + '" aria-valuenow="' + d + '">' + segs + '</div>';
  };

  App.prototype.viewFooter = function () {
    var st = this.state;
    return '<footer class="fpr-foot">' +
      '<p>These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease. Results may vary.</p>' +
      '<p>Your check-ins are saved on this device only. On iPhone, Safari may clear them if you don\'t open this page for 7+ days.' +
      (st && st.consent && st.email ? ' Reminders go to ' + esc(st.email) + '.' : '') + '</p></footer>';
  };

  App.prototype.viewSettings = function () {
    var st = this.state;
    return '<details class="fpr-card fpr-settings"><summary>Edit my plan</summary>' +
      '<fieldset class="fpr-q"><legend>Main goal</legend><div class="fpr-chips">' +
        Object.keys(GOALS).map(function (k) { return chip('set', 'goal', k, GOALS[k].label, st.goal === k); }).join('') + '</div></fieldset>' +
      '<fieldset class="fpr-q"><legend>Bottles ordered</legend><div class="fpr-chips">' +
        BOTTLES.map(function (o) { return chip('set', 'bottles', o[0], o[1], String(st.bottles) === o[0]); }).join('') + '</div></fieldset>' +
      '<fieldset class="fpr-q"><legend>Capsules a day</legend><div class="fpr-chips">' +
        CAPS.map(function (o) { return chip('set', 'capsPerDay', o[0], o[1], String(st.capsPerDay) === o[0]); }).join('') + '</div></fieldset>' +
      '<fieldset class="fpr-q"><legend>Capsule goes with</legend><div class="fpr-chips">' +
        MEALS.map(function (o) { return chip('set', 'meal', o[0], o[1], st.meal === o[0]); }).join('') + '</div></fieldset>' +
      '<label class="fpr-field"><span>Your why</span><textarea rows="2" maxlength="140" data-why placeholder="What will be different when you feel better?">' + esc(st.why) + '</textarea></label>' +
      '<p class="fpr-small">Changing these keeps all your check-ins.</p>' +
      '<button type="button" class="fpr-link fpr-danger" data-action="restart">Start over and clear my data</button></details>';
  };

  App.prototype.viewCheckin = function (d) {
    var st = this.state;
    var target = this.ciDay || d;
    var c = st.checkins[target];
    var canYesterday = !this.ciDay && d >= 2 && !st.checkins[d - 1];
    var yesterdayLink = canYesterday ? '<button type="button" class="fpr-link" data-action="log-yesterday">Missed yesterday? Add Day ' + (d - 1) + '</button>' : '';

    if (c && !this.editing) {
      return '<section class="fpr-card fpr-checkin fpr-done">' +
        '<div class="fpr-card-top"><h2 class="fpr-h3">Today\'s check-in</h2><span class="fpr-badge">' + icon('check') + 'Done</span></div>' +
        '<div class="fpr-scores">' + METRICS.map(function (m) {
          return '<div class="fpr-m-' + m.id + '"><span>' + m.label + '</span><strong>' + c[m.id] + '</strong><i style="width:' + (c[m.id] * 10) + '%"></i></div>';
        }).join('') + '</div>' +
        '<p class="fpr-win"><span>' + icon('peak') + '</span><span><strong>Today\'s win</strong>' + this.winFor(target) + '</span></p>' +
        '<div class="fpr-links"><button type="button" class="fpr-link" data-action="edit-checkin">Edit today</button>' + yesterdayLink + '</div></section>';
    }

    var n = st.capsPerDay;
    if (!this.ci) {
      var prev = c || this.lastBefore(target);
      var taken = c ? capsTaken(c) : 0;
      this.ci = prev ? { sleep: prev.sleep, calm: prev.calm, energy: prev.energy } : { sleep: 5, calm: 5, energy: 5 };
      this.ci.caps = [];
      for (var i = 0; i < n; i++) this.ci.caps.push(i < taken);
      this.ci.gut = c ? !!c.gut : false;
    }
    var ci = this.ci;
    var first = !this.days().length;
    var isPast = target < d;
    var title = isPast ? 'Yesterday · Day ' + target : (first ? 'Your Day ' + target + ' baseline' : 'How are you today?');
    var sub = isPast ? 'How was yesterday? Best guess is fine.' :
      (first ? 'Be honest. This is the starting point you\'ll compare against.' :
        (this.lastBefore(target) ? 'Starts from your last check-in. Move only what changed.' : '10 seconds. Slide, tap, save.'));
    var capLabels = n === 1 ? ['Took my capsule with ' + this.mealLabel()] : ['Capsule 1, with ' + this.mealLabel(), 'Capsule 2, at another meal'];
    return '<section class="fpr-card fpr-checkin">' +
      '<h2 class="fpr-h3">' + title + '</h2>' +
      '<p class="fpr-sub">' + sub + '</p>' +
      METRICS.map(function (m) {
        return '<label class="fpr-range fpr-m-' + m.id + '"><span class="fpr-range-top"><span>' + m.label + '</span><output data-out="' + m.id + '">' + ci[m.id] + '</output></span>' +
          '<input type="range" min="1" max="10" step="1" value="' + ci[m.id] + '" data-metric="' + m.id + '" aria-label="' + m.label + ', 1 to 10">' +
          '<span class="fpr-range-ends" aria-hidden="true"><small>' + m.low + '</small><small>' + m.high + '</small></span></label>';
      }).join('') +
      '<div class="fpr-pills">' +
        capLabels.map(function (l, i) {
          return '<button type="button" class="fpr-pill' + (ci.caps[i] ? ' is-on' : '') + '" data-action="cap" data-value="' + i + '" aria-pressed="' + !!ci.caps[i] + '">' + icon('capsule') + '<span>' + l + '</span></button>';
        }).join('') +
        '<button type="button" class="fpr-pill fpr-pill-warn' + (ci.gut ? ' is-on' : '') + '" data-action="gut" aria-pressed="' + !!ci.gut + '">' + icon('tummy') + '<span>Stomach felt off</span></button>' +
      '</div>' +
      '<button type="button" class="fpr-btn" data-action="save-checkin">' + (isPast ? 'Save Day ' + target : 'Save check-in') + '</button>' +
      '<div class="fpr-links">' + (isPast || this.editing ? '<button type="button" class="fpr-link" data-action="cancel-checkin">Cancel</button>' : '') + yesterdayLink + '</div>' +
      '</section>';
  };

  App.prototype.viewHabit = function (d) {
    var st = this.state;
    if (d > CORE_DAYS && !st.unlocked) {
      return '<section class="fpr-card fpr-locked">' +
        '<div class="fpr-card-top"><span class="fpr-eyebrow">' + icon('lock', 'fpr-ico-sm') + ' Phase 4 · Stay</span></div>' +
        '<p class="fpr-habit-text">New daily habits for <span class="fpr-nowrap">days 46–90</span>.</p>' +
        '<p class="fpr-small">Included with 2+ bottle orders. Your code is in your order confirmation email. Your check-ins keep working either way.</p>' +
        this.viewUnlockForm() +
        '<a class="fpr-btn fpr-btn-ghost" href="' + esc(this.productUrl) + '">See bottle bundles</a></section>';
    }
    var done = !!st.habits[d];
    var label = d > CORE_DAYS ? 'Stay' : GOALS[st.goal].label;
    return '<section class="fpr-card fpr-habit' + (done ? ' is-done' : '') + '">' +
      '<div class="fpr-card-top"><span class="fpr-eyebrow">' + icon(st.goal, 'fpr-ico-sm') + ' Today\'s habit · ' + label + '</span></div>' +
      '<p class="fpr-habit-text">' + this.habit(d) + '</p>' +
      '<button type="button" class="fpr-toggle' + (done ? ' is-on' : '') + '" data-action="habit" aria-pressed="' + done + '">' +
        '<span class="fpr-box">' + icon('check') + '</span>' + (done ? 'Done for today' : 'Mark as done') + '</button>' +
      // Reward for finishing: a peek at tomorrow, so there is a reason to come back.
      (done && d + 1 <= this.limit() ? '<p class="fpr-tomorrow"><strong>Tomorrow:</strong> ' + this.habit(d + 1).replace(/\btonight\b/g, 'tomorrow night').replace(/\btoday\b/g, 'tomorrow') + '</p>' : '') +
      '</section>';
  };

  App.prototype.viewMilestone = function (d) {
    var dl = this.deltas();
    var end = (d > CORE_DAYS && d <= CORE_DAYS + 3) ? 45 : ((d > MAX_DAYS && d <= MAX_DAYS + 3) ? 90 : 0);
    if (!end) return '';
    var html = '<section class="fpr-card fpr-complete"><span class="fpr-eyebrow">' + icon('check', 'fpr-ico-sm') + ' Milestone</span>' +
      '<h2 class="fpr-h2">' + (end === 45 ? 'You finished Start, Build and Keep' : 'You finished all 90 days') + '</h2>';
    if (dl) {
      html += '<p class="fpr-sub">Day ' + dl.from + ' vs your last 3 check-ins</p><div class="fpr-scores">' + METRICS.map(function (m) {
        var x = dl[m.id];
        return '<div class="fpr-m-' + m.id + '"><span>' + m.label + '</span><strong>' + x.now.toFixed(1) + '</strong><em class="' + dirClass(x.diff) + '">' + fmtDelta(x.diff) + '</em></div>';
      }).join('') + '</div>';
    }
    html += '<p class="fpr-keep">' + (end === 45
      ? 'The first 45 days built it. The next 45 keep it. Your body uses magnesium every day, so the routine is what holds on to your progress.'
      : 'Ninety days of showing up. Keep the capsule and the 2 or 3 habits that worked: that is how this becomes your normal.') + '</p>';
    return html + '</section>';
  };

  App.prototype.viewNudges = function (d) {
    var st = this.state, html = '';
    var supply = this.supplyDays();
    var left = supply - d + 1;
    if (left >= 1 && left <= 12) {
      html += '<section class="fpr-card fpr-nudge"><h2 class="fpr-h3">About ' + left + ' day' + (left === 1 ? '' : 's') + ' of capsules left</h2>' +
        '<p>' + this.builtSoFar() + 'Running out is the easiest way to lose a routine. Shipping takes about a week, so order now and your next bottle arrives before this one ends.</p>' +
        '<a class="fpr-btn" href="' + esc(this.productUrl) + '">See refill options</a></section>';
    } else if (left <= 0 && left > -10) {
      html += '<section class="fpr-card fpr-nudge"><h2 class="fpr-h3">Out of capsules?</h2>' +
        '<p>Your body keeps using magnesium every day, capsule or not. Keep checking in, and restock to pick up right where you left off: your streak, your chart and your plan are all still here.</p>' +
        '<a class="fpr-btn" href="' + esc(this.productUrl) + '">Restock PeakMag</a></section>';
    }
    // Digestive discomfort is the #1 reason people quit magnesium: catch it early.
    var recent = this.days().slice(-3), gutDays = recent.filter(function (x) { return st.checkins[x].gut; });
    if (gutDays.length >= 2 && (+st.tips.gut || 0) < gutDays[gutDays.length - 1]) {
      html += '<section class="fpr-card fpr-info fpr-care"><h2 class="fpr-h3">Stomach feeling off?</h2>' +
        '<p>It happens to some people with magnesium. Take your capsule with a meal' + (st.capsPerDay === 2 ? ', and go back to 1 a day for a week' : '') + '. Still not right after a few days? <a href="' + esc(this.contactUrl) + '">Message us</a>, we\'ll help.</p>' +
        '<button type="button" class="fpr-btn fpr-btn-ghost" data-action="dismiss-tip" data-value="gut">Got it</button></section>';
    }
    if (d === 7 || d === 21) {
      var next = this.phase(d + 1);
      html += '<section class="fpr-card fpr-info"><h2 class="fpr-h3">Last day of Phase ' + this.phase(d).id + '</h2>' +
        '<p>Tomorrow: <strong>' + next.name + '</strong>. ' + next.text + '</p></section>';
    }
    if (!st.tips.home && this.days().length >= 1) {
      html += '<section class="fpr-card fpr-info"><h2 class="fpr-h3">Make it a 10-second habit</h2>' +
        '<p>Save this page to your home screen so it\'s one tap away tomorrow.</p>' +
        '<ul class="fpr-howto"><li><strong>iPhone:</strong> tap Share, then "Add to Home Screen".</li><li><strong>Android:</strong> tap ⋮, then "Add to Home screen".</li></ul>' +
        '<button type="button" class="fpr-btn fpr-btn-ghost" data-action="dismiss-tip" data-value="home">Done, hide this</button></section>';
    }
    return html;
  };

  App.prototype.viewUnlockForm = function () {
    return '<div class="fpr-unlock"><input type="text" placeholder="Enter your code" autocapitalize="characters" autocomplete="off" spellcheck="false" data-unlock-input aria-label="Phase 4 code" value="' + esc(this.unlockDraft) + '">' +
      '<button type="button" class="fpr-btn" data-action="unlock">Unlock</button></div>' +
      (this.unlockError ? '<p class="fpr-hint" role="alert">' + this.unlockError + '</p>' : '');
  };

  App.prototype.viewProgress = function () {
    var days = this.days();
    if (!days.length) return '';
    var dl = this.deltas();
    var html = '<section class="fpr-card"><h2 class="fpr-h3">Your progress</h2>';
    if (dl) {
      html += '<div class="fpr-deltas">' + METRICS.map(function (m) {
        var x = dl[m.id];
        return '<div class="fpr-delta fpr-m-' + m.id + '"><span>' + m.label + '</span><strong class="' + dirClass(x.diff) + '">' + fmtDelta(x.diff) + '</strong><small>vs Day ' + dl.from + '</small></div>';
      }).join('') + '</div>';
    } else {
      html += '<p class="fpr-sub">Check in tomorrow to see your first trend.</p>';
    }
    return html + this.chart() + '</section>';
  };

  App.prototype.chart = function () {
    var st = this.state, d = this.day();
    var s = Math.max(1, d - (MAX_DAYS - 1));
    var e = Math.max(s + 6, d);
    var span = e - s + 1;
    var smooth = span > 21;
    var W = 300, H = 170, L = 22, R = 6, T = 8, B = 26;
    function x(n) { return L + (n - s) * (W - L - R) / (span - 1); }
    function y(v) { return T + (10 - v) * (H - T - B) / 9; }
    function val(n, id) {
      if (!st.checkins[n]) return null;
      if (!smooth) return st.checkins[n][id];
      var sum = 0, k = 0;
      for (var i = n - 2; i <= n; i++) if (st.checkins[i]) { sum += st.checkins[i][id]; k++; }
      return sum / k;
    }
    var g = '';
    [1, 5, 10].forEach(function (v) {
      g += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y(v) + '" y2="' + y(v) + '" class="fpr-grid"/><text x="' + (L - 6) + '" y="' + (y(v) + 4) + '" text-anchor="end" class="fpr-axis">' + v + '</text>';
    });
    [[s, 'start'], [Math.round((s + e) / 2), 'middle'], [e, 'end']].forEach(function (a) {
      g += '<text x="' + x(a[0]) + '" y="' + (H - 6) + '" text-anchor="' + a[1] + '" class="fpr-axis">Day ' + a[0] + '</text>';
    });
    METRICS.forEach(function (m) {
      var path = '', prev = false, dots = '';
      for (var n = s; n <= e; n++) {
        var v = val(n, m.id);
        if (v == null) { if (!smooth) prev = false; continue; }
        path += (prev ? 'L' : 'M') + x(n).toFixed(1) + ' ' + y(v).toFixed(1);
        if (!smooth) dots += '<circle cx="' + x(n).toFixed(1) + '" cy="' + y(v).toFixed(1) + '" r="3"/>';
        prev = true;
      }
      g += '<g class="fpr-line fpr-m-' + m.id + '"><path d="' + path + '"/>' + dots + '</g>';
    });
    var legend = '<div class="fpr-legend">' + METRICS.map(function (m) { return '<span class="fpr-m-' + m.id + '"><i></i>' + m.label + '</span>'; }).join('') +
      (smooth ? '<span class="fpr-legend-note">3-day average</span>' : '') + '</div>';
    return '<svg class="fpr-chart" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Daily scores for sleep, calm and energy, days ' + s + ' to ' + e + '">' + g + '</svg>' + legend;
  };

  App.prototype.viewJourney = function (d) {
    var st = this.state, self = this;
    return '<section class="fpr-card"><h2 class="fpr-h3">Your journey</h2><ol class="fpr-journey">' +
      PHASES.map(function (p) {
        var locked = p.bonus && !(st && st.unlocked);
        var status = d > p.to ? 'is-past' : (d >= p.from ? 'is-now' : '');
        var extra = '';
        // The unlock field lives here only until day 45; after that it moves to the Phase 4 card (never both).
        if (p.bonus && st && st.start && !st.unlocked && self.day() <= CORE_DAYS) extra = '<p class="fpr-small">Included with 2+ bottle orders. Have a code?</p>' + self.viewUnlockForm();
        else if (p.bonus && locked) extra = '<p class="fpr-small">Bonus, included with 2+ bottle orders.</p>';
        return '<li class="' + status + (locked ? ' is-locked' : '') + '">' +
          '<span class="fpr-step">' + (locked ? icon('lock') : (d > p.to ? icon('check') : p.id)) + '</span>' +
          '<div><small>Day ' + p.from + '–' + p.to + (p.bonus ? ' · Bonus' : '') + '</small><strong>' + p.name + '</strong><p>' + p.text + '</p>' + extra + '</div></li>';
      }).join('') + '</ol></section>';
  };

  App.prototype.viewDebug = function () {
    var st = this.state;
    var live = !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
    return '<section class="fpr-debug' + (live ? ' is-live' : '') + '"><strong>' + (live ? 'DEBUG MODE IS ON. Visitors can see this panel: turn it off in the theme editor.' : 'Debug (preview)') + '</strong>' +
      (st && st.start ? '<div><button type="button" data-action="dbg-shift" data-n="1">+1 day</button><button type="button" data-action="dbg-shift" data-n="7">+7 days</button><button type="button" data-action="dbg-shift" data-n="-1">−1 day</button><button type="button" data-action="dbg-fill">Fill past check-ins</button></div>' +
        (this.lastTags ? '<p>Last tags: ' + esc(this.lastTags) + '</p>' : '') : '<p>Finish onboarding (and start Day 1) to enable the day simulator.</p>') +
      '</section>';
  };

  function boot() {
    var roots = document.querySelectorAll('[data-fpr]');
    for (var i = 0; i < roots.length; i++) {
      if (!roots[i].__fpr) roots[i].__fpr = new App(roots[i]);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
  // Re-init when the section is re-rendered inside the theme editor.
  document.addEventListener('shopify:section:load', boot);
})();
