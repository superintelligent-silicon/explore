---
title: "Defrost Mode"
description: "In October 2026 hackers cooked the food in hundreds of French supermarkets by switching their fridges to defrost. What happened, what it means for the connected devices in your home, and simple steps to stay safe."
author: Superintelligent Silicon
published: 2026-10-18
updated: 2026-10-18
canonical: https://exploresuperintelligence.online/articles/defrost-mode/
---

# Defrost Mode

*One night in October, hackers took over the fridges in hundreds of French supermarkets and left them on defrost until morning. Here's what happened, and what it means for the connected devices in your home.*

By Superintelligent Silicon. Updated October 18, 2026. The interactive edition, with the risk map, decision wizard and checklist, is at https://exploresuperintelligence.online/articles/defrost-mode/

## The short version

- **~700** of France's ~10,000 supermarkets were hit, per its finance minister.
- **50°C** (122°F) in the cases for hours; one store hit 80°C, the Guardian reports.
- **Old and online:** out-of-date controls that anyone online could reach.
- **Your home:** the same weak spots: old software, shared passwords.

Five things worth doing:

1. **Make a list.** Every connected device, its app, and who else can sign in.
2. **Disconnect what you don't use.** No connection means no remote risk, and it costs nothing.
3. **Lock down the rest.** A unique password and two-step sign-in for every account.
4. **Retire the risky stuff.** No-name streaming boxes, recalled heaters, heaters on smart plugs.
5. **Add backups that don't need the internet.** Leak sensors that shut off the water, a fridge alarm, smoke alarms.

## A night stuck in defrost

*01 · What happened*

Each store's fridges run on one small control computer that repair firms reach online. Attackers got in and set it to defrost all night.

- **Oct 11–12:** Overnight, fridges at Intermarché, Coopérative U, Carrefour, Monoprix, Leclerc and others are switched to defrost and left there.
- **Oct 12:** Paris prosecutors open an inquiry, citing spoiled food and fires. Danfoss, which makes the controls, says the hit units ran old or unsupported software.
- **Oct 13:** France's cyber-emergency team adds two more makers, Copeland and Dixell. About 700 of France's 10,000 supermarkets were hit, the finance minister says.
- **Oct 16:** Its updated advice: allow remote access only over a private, encrypted link, and check defrost schedules.
- **Oct 17:** One Normandy store's freezers reached 80°C, and nobody has claimed the attack, the Guardian reports.

### Confirmed vs unknown

*Updated October 18, 2026*

**Equipment.** Confirmed. Danfoss store controls (AK-SM and AK-SC models), and from October 13 controls from Copeland and its Dixell brand, according to France's cyber-emergency team, CERT-FR.

**Scale.** About 700 of France's roughly 10,000 supermarkets, Finance Minister Roland Lescure told lawmakers, as AP reported on October 13. Early counts were 300 to 350.

**Condition.** Danfoss says the hit units ran old software or were no longer supported.

**How they got in.** Unknown. Claroty published Danfoss flaws in August, but no official source has tied them to this attack.

**Who did it.** Unknown. As of October 17, no individual or group had claimed it, the Guardian reported.

**Still going?** Possibly. CERT-FR's October 16 update says attacks on these controls are probably still running.

**Heat and fires.** Intermarché says its fridges ran at 50°C for six hours. The Guardian reported one Normandy store's freezers reached 80°C, and sprinklers caused water damage in some stores. The Paris prosecutor reported fires; some coverage blames defrost heaters left running, which isn't officially confirmed.

**Beyond France.** Unclear. Albert Heijn's parent company had a separate security incident the same day, with no established link.

### Exposed online

On October 12, Predicta Lab's Baptiste Robert counted **2,752** Danfoss systems reachable from the internet, **1,590** of them in France. Shodan, a search engine for internet-connected devices, was tracking **more than 4,500**.

Exposed doesn't mean hacked, or even vulnerable. It means the login page could be reached by anyone, which is what an attack like this needs.

France's cyber-emergency team told stores to take these controls off the public internet. The same idea works at home: a device you never need to reach from outside shouldn't be reachable from outside.

## Easy to reach, out of date, and trusted

*02 · Why it worked*

None of it took a genius, and each weakness has an everyday version at home. Tap one to compare.

- **Reachable from anywhere.** In the French stores: The controls had login pages on the open internet, so repair firms could adjust them from anywhere. At home: Smart devices that take orders from anyone, anywhere, who has the password.
- **Out-of-date software.** In the French stores: Danfoss says the units that were hit ran old software or were no longer supported. At home: Appliances last ten years or more, but makers often stop sending security fixes much sooner.
- **Weak sign-in.** In the French stores: Security firm Claroty found a hidden backup login on one Danfoss model, based on the date and fixed in a later update; no one has tied it to this attack. An expert quoted by the Guardian said many freezers seemed to be running on a default password. At home: Reused passwords, factory-default passwords, and no two-step sign-in.
- **Access through someone else.** In the French stores: Retailers point to the outside contractors who maintain their refrigeration, not the stores themselves. At home: Installers, past housemates or a previous owner who can still open the app.
- **A normal command nobody questioned.** In the French stores: Defrost is a routine setting, so the systems ran it for hours overnight. Early findings suggest alarms were switched off first, the Guardian reports. At home: A device that can be started remotely, in a home where nobody is around to notice.
- **Warnings not acted on.** In the French stores: The U.S. cyber agency CISA warned about a Danfoss flaw in 2025, Claroty published research in August 2026, and fixes existed. At home: Update prompts and recall notices that get ignored or land in spam.

## Five ways in, three safety nets

*03 · How devices get taken over*

- **App account.** In 2017 Check Point found a flaw in LG's SmartThinQ sign-in that let attackers take over accounts and every linked appliance, from ovens to washers. LG fixed it within two months. Today the bigger risk is plainer: one reused password, leaked from some other site, opens every appliance on the account.
- **Shared access.** In France, retailers pointed to the outside contractors who maintain their fridges, not the stores themselves. At home, the same app login is often shared by family, an installer or a house-sitter, and sometimes by a previous owner who was never removed.
- **Maker's servers.** Most apps reach your appliance through the manufacturer's servers rather than directly. One break-in there can reach every device on that service at once.
- **Home Wi-Fi.** Anything on your Wi-Fi can talk to the other devices on it: a visitor's phone, an infected laptop, a cheap gadget. Putting smart devices on their own network, which many routers call a guest network, keeps them apart from your phones and laptops.
- **Linked apps.** June blamed a link with Amazon's Alexa for one of its ovens preheating overnight. University of Michigan researchers used a smart-home add-on with more permissions than it needed to add their own code to a door lock.
- **The device itself.** The controls in France worked exactly as designed and followed a command that looked normal. So any device that can be controlled remotely should be judged by what it would do if the wrong person sent a normal-looking command.
- **Switched on at the machine.** A U.S. safety standard (UL 858) requires smart ranges to have remote use switched on by hand at the appliance. Washers and dryers need a button press with the door closed, and opening the door cancels remote start.
- **Hardware cutoffs.** A dryer's heat cutoff switches and a dishwasher's float switch react to temperature and water level, whatever the app says. They're why remote fires and floods are unlikely on name-brand machines.
- **Independent sensors.** Leak sensors tied to an automatic shutoff valve, fridge and freezer alarms, and smoke alarms that reach a real person all catch trouble even when the device itself has been fooled.

## The usual weak spots

*04 · What researchers keep finding*

Ranked by how likely each one is. Orange shows the risk today, the blue outline after the fix.

1. **Cheap gadgets that arrive infected** (Off-brand streaming boxes, projectors, tablets, photo frames). Likelihood: Likely now, Rare after the fix; impact Moderate. The FBI warned in June 2025 that a criminal network called BadBox 2.0 had infected more than a million devices, many of them at the factory. They quietly pass criminals' internet traffic through the owner's connection. Warning signs: unknown brands, and streaming boxes sold as "unlocked" or promising free content. **Fix:** Swap off-brand boxes, projectors and frames for major brands.
2. **Weak or shared passwords** (Appliance apps, locks, cameras, thermostats). Likelihood: Likely now, Unlikely after the fix; impact Severe. Reused passwords, no two-step sign-in, and one account shared by everyone. A single stolen password then controls every device on it. **Fix:** A unique password and two-step sign-in for every account, and a separate login for each person where the app allows it.
3. **Old accounts still linked** (Thermostats, locks, alarms, doorbells). Likelihood: Likely now, Unlikely after the fix; impact Severe. When a home changes hands, the old account often stays attached. Homebuyers have reported thermostats adjusting themselves because the seller was still linked, and alarm systems they couldn't control. **Fix:** When you move in, or change installers, remove the old accounts, and check each app's list of users now and then.
4. **Security updates that end early** (Smart washers, dishwashers, fridges, TVs). Likelihood: Expected now, Unlikely after the fix; impact Moderate. The UK consumer group Which? found most appliance makers wouldn't commit to a support period. Some promised only two years; Miele promised ten. Big appliances usually last 10 to 11 years, so support ending first is close to certain. **Fix:** Check how long updates are promised before you buy, and disconnect or replace a device once they stop.
5. **One cheap gadget, many brand names** (Budget plugs, bulbs, heaters, switches). Likelihood: Possible now, Rare after the fix; impact Moderate. One test of cheap smart plugs found the same default password, 12345678, on every unit, unencrypted traffic, and a way to load malicious software for under £5. Dozens of brands often share one factory's design. **Fix:** Swap them for known brands, or for gear that works without an online account.
6. **Building controls left online** (Heating, pool, gate and building systems). Likelihood: Unlikely now, Unlikely after the fix; impact Severe. This is the closest thing to the French case: a login page anyone can find, running old software. In apartment blocks and offices these systems usually belong to the building, so the fix is a question rather than a setting. **Fix:** If you live or work in a shared building, ask the manager whether these controls can be reached from the internet, and ask them to close that off.

## Risk follows heat, water and doors

*05 · Device by device*

| Device | Risk | Likelihood now / after fix | Impact | Worst realistic outcome | What normally stops it | The fix |
|---|---|---|---|---|---|---|
| Smart plug on a heater | High | Possible / Rare | Severe | A heater, iron, kettle or coffee maker switched on for hours with nobody home. | Nothing. A smart plug just switches power and has no idea what's plugged into it. | Never put anything that heats on a smart plug. |
| Smart space heater | High | Possible / Rare | Severe | Turns itself on, and could start a fire. | Depends on the brand. Govee recalled about 512,500 heaters that could overheat because of their wireless controls, and Atomi about 99,400 that could switch on by themselves. | Check the U.S. product-safety recall list (CPSC) and stop using any recalled model. |
| Off-brand streaming box | High | Likely / Rare | Moderate | Quietly used to pass criminals' traffic through your internet connection, with a foothold on your network. | Nothing, when the malware came installed at the factory. | Swap it for a major-brand streaming stick or the TV's own apps. |
| Smart lock | High | Likely / Unlikely | Severe | The door unlocked, or extra codes added. | Only the account's security and how codes are managed. | Give each person their own code, check the lock's activity history, and delete codes nobody needs. |
| Camera or doorbell | High | Possible / Unlikely | Severe | A stranger watching a live view of your home. | Only the account's security. | Turn on two-step sign-in and remove shared users you don't recognise. |
| Wi-Fi router | High | Possible / Unlikely | Severe | A default admin password lets someone change settings, watch traffic, or reach every device on your network. | Only its admin password and its updates. | Change the admin password, keep it updated, turn off remote admin, and use a separate network for visitors and smart devices. |
| Countertop smart oven | Medium | Possible / Rare | Severe | Heats up empty or with clutter inside. Three June ovens preheated themselves overnight to 400°F or more in 2019. | Lighter safety rules than built-in ranges. | Unplug it when you're away. |
| Fridge and freezer | Medium | Unlikely / Rare | Moderate | Temperature raised or defrost forced, so food spoils quietly. | Very little, because warm is a valid setting. | Disconnect it if you don't use the app, and add a cheap standalone temperature alarm. |
| Thermostat | Medium | Possible / Unlikely | Moderate | Heating or cooling switched off while you're away, so damp, mold or frozen pipes can follow. | Usually nothing beyond the lowest and highest settings. | Turn on temperature alerts, set limits, and remove old users. |
| Smart TV | Medium | Likely / Unlikely | Moderate | Aging software and old logins left signed in. | Major brands send updates for a few years. | Keep it updated and sign out of accounts you no longer use. |
| Built-in range | Low | Rare / Rare | Severe | Preheated remotely with something left inside. | A U.S. safety standard (UL 858) requires remote use to be switched on by hand at the range, and many brands block remote starts on the cooktop entirely. | Leave remote mode off, and don't store things in the oven. |
| Dryer | Low | Rare / Rare | Moderate | Runs with a lint-choked vent. | Remote start has to be switched on at the machine with the door shut, and a heat cutoff switch works whatever the app says. | Clean the lint trap and vent regularly, and leave remote mode off. |
| Washer | Low | Rare / Rare | Moderate | Runs a cycle; leaks if a hose fails. | Remote start must be switched on at the machine, opening the door cancels it, and the overflow controls work on their own. | Braided steel hoses, a leak sensor and an automatic shutoff valve. |
| Dishwasher | Low | Rare / Rare | Minor | Runs a cycle. | A float switch shuts off the water and drains it if the level rises too far. | A leak sensor under the sink. |
| Water shutoff valve | Low | Unlikely / Rare | Minor | Water shut off, or alerts silenced. | It can only close or reopen the supply. | Keep it, and protect its app login like a door lock's. |

### How we rate likelihood

Each rating is our judgment of the chance that a device or weak spot gets misused in a typical home over the next few years, based on the incidents and research cited here. There's no public data on how often home devices are actually compromised, so treat these as a guide to priorities, not as odds.

**Rare.** Needs unusual skill or a chain of failures, with no known cases in homes.

**Unlikely.** Shown in research or isolated cases, but the conditions are uncommon.

**Possible.** Has happened in real homes, and many homes have the conditions for it.

**Likely.** The conditions are common, so it's more likely than not over a few years.

**Expected.** It happens unless you act. Security updates ending is the clearest case.

**Impact.** **Minor** is an inconvenience, **Moderate** is money or privacy lost, and **Severe** means fire, flooding, a break-in or a safety risk.

## Most break-ins still use force

*07 · Smart and keypad locks*

Every lock has a known weakness, but most burglars simply kick or pry. Bars show the break-in odds now, blue after the fix.

- **Name-brand smart lock** (Schlage, Yale, August, Kwikset, Master Lock). Verdict: Good pick. Break-in likelihood Unlikely now, Rare after the fix. A 2025 study of Master Lock's D1000 found shared access that kept working about nine months after it was taken away. The company planned fixes. Real weak point: Codes and app access that never really expire. **Fix:** Keep it updated, and test that deleted codes actually stop working.
- **No-name smart lock** (Marketplace fingerprint and tap-card locks). Verdict: Avoid. Break-in likelihood Possible now, Rare after the fix. Researchers at Secura removed one model's fingerprint reader with two screws and added their own fingerprint in about five minutes. Its tap cards could be copied. Real weak point: Weak hardware and cards that can be cloned. **Fix:** Replace it with a name-brand lock.
- **Push-button keypad lock** (Kaba Simplex (now dormakaba)). Verdict: Check it. Break-in likelihood Possible now, Unlikely after the fix. In 2010 Kaba learned that a magnet costing about $30 could open several Simplex models, and in 2011 it offered owners a free fix kit. Real weak point: Codes lots of people know, because changing one takes a tool. **Fix:** Confirm the magnet fix is fitted, and change the code when people move on.
- **Hotel and apartment card locks** (dormakaba Saflok). Verdict: Check it. Break-in likelihood Possible now, Unlikely after the fix. The 2024 "Unsaflok" research showed one card could be used to make a pair that opens every door at a property. More than 3 million doors at 13,000 properties were affected, and only about 36% had been updated by March 2024. Real weak point: Systems that haven't been updated. The deadbolt doesn't stop a forged card. **Fix:** Ask the building whether the upgrade is done, and use the chain or swing bar when you're inside.
- **Plain keyed deadbolt** (Any brand). Verdict: Backup. Break-in likelihood Possible now, Unlikely after the fix. It can be picked or bumped, and keys get copied. Real weak point: Short screws in the strike plate, so a kick tears the frame. **Fix:** Fit a four-screw strike plate with 3-inch screws, and keep it as your backup lock.

### What actually secures a door

1. **Reinforce the frame.** A heavy-duty strike plate with four 3-inch screws into the wall stud does more against a kick than any lock upgrade.
2. **Make access expire.** Give each person their own code, and delete it when they no longer need it.
3. **Buy a grade, not a brand.** Look for a BHMA Grade 1 or 2 deadbolt on outside doors.
4. **Keep a mechanical backup.** A key or keyed deadbolt means a dead battery or a hacked lock isn't your last line.
5. **Use the chain or swing bar.** Especially in hotels and apartments with card locks, as the Unsaflok researchers recommend.

## What to worry about

*08 · Keeping perspective*

**Overhyped**

- **A hacker flooding your home through the washer** (Rare). Remote start must be switched on at the machine, and the overflow controls work without the Wi-Fi.
- **Remote dryer fires** (Rare). The heat cutoff trips on temperature, not on what the app says. Lint and blocked vents are still the real cause.
- **Someone targeting your home in particular** (Unlikely). Attacks like France's find a whole class of exposed, out-of-date devices and hit them all at once.
- **The ESP32 chip "backdoor"** (Rare). A real 2025 finding about a common Wi-Fi chip, but abusing it needs code already running on the device.

**Real**

- **Quiet sabotage** (Possible). A warm fridge, heating switched off or a silenced alarm does damage nobody notices until later.
- **Devices with no safety layer** (Possible). Smart plugs and cheap smart heaters do whatever they're told.
- **Locks and cameras** (Likely). A lock or camera account is a key, and a window into your home.
- **A whole product line hit at once** (Possible). The French attack reached hundreds of stores at once because they ran the same out-of-date controls.
- **Faults with nobody home** (Likely). Remote features fail on their own, and an empty home lets a small fault run for days.

## Keep, disconnect, replace or remove

*09 · Decide, one device at a time*

Throwing out a working fridge because it has Wi-Fi is usually a waste. Three questions settle almost every device.

1. Is it off-brand, recalled, or something that heats running on a smart plug? **Yes: remove it now.**
2. Do you actually use its smart features? **No: disconnect it.**
3. Is the maker still sending it security updates? **Yes: keep it, locked down. No: replace it** (or disconnect it and live without the feature).

## Cut the connection, keep the appliance

*10 · Make it dumb again*

The computer inside runs the machine, so it stays. What you can remove is its link to the internet.

1. **Never connect it.** Skip the app setup, or never give it the Wi-Fi password. You give up: Remote features only. Reversible: Yes.
2. **Disconnect and unregister.** Remove it from the app account, reset its Wi-Fi settings, then change your Wi-Fi password so it can't rejoin. About ten minutes. You give up: Remote features only. Reversible: Yes.
3. **Block it at the router.** Use your router's app or device list to cut that appliance off from the internet. You give up: Remote features, and over time its updates. Reversible: Yes.
4. **Turn the radio off.** Some models have a Wi-Fi off switch in settings or a service menu. Many don't, and on some the radio comes back after a reset. You give up: Remote features. Reversible: Yes.
5. **Unplug the Wi-Fi module.** On many appliances the Wi-Fi is a small separate board. GE sells its Connect Module as a plug-in part, and LG and Samsung list Wi-Fi boards as separate parts. A technician can disconnect it. You give up: Remote features. Some models show an error code, and it may affect the warranty. Reversible: Usually, by plugging it back in.

**The catch:** some cycles only exist in the app. Bosch's 500-series dishwashers put Rinse, Eco and Delay Start there, so a disconnected one loses them. For most people the standard cycles are enough.

## Stop water before it spreads

*11 · Water, the expensive one*

A hacked appliance rarely floods a home, but an ordinary leak often does. Here's every way to catch one, cheapest first.

- **1 in 60** insured homes file a water or freeze claim each year.
- **$12.5k** average claim, 2017–2021.
- **~24%** of all homeowner claims in 2021.

### Leak alarms with a siren (Low)

Sounds an alarm · works offline. A battery puck on the floor that sounds a loud alarm when it touches water. No app, no Wi-Fi.

Pluses: Nothing to set up and nothing to hack; Keeps working through power and internet outages; Cheap enough to put everywhere.

Minuses: Only helps if someone hears it; Doesn't stop the water; Only detects water right where it sits.

Best for: Fine where someone will hear it, but no help when nobody's home. If someone took it over: Nothing to take over.

### Smart leak sensors (~$50 for 4)

Phone alerts and a siren. Battery sensors that alert your phone and sound a siren. Some connect to Wi-Fi directly and others through a small hub; YoLink's hub-and-four-sensor kit sells for about $50, and its sensors run about five years on AAA batteries.

Pluses: Inexpensive and quick to place; Alerts reach you while you're away; Some kits can trigger a shutoff valve or cut power to the washer.

Minuses: Doesn't stop the water on its own; Phone alerts need Wi-Fi and internet; Batteries to change, and false alarms where water splashes; Someone still has to respond, and fast.

Best for: The baseline for most homes, with alerts going to someone who can get there quickly. If someone took it over: Someone could silence alerts or send false ones: annoying, not dangerous.

### Appliance shutoffs (~$290 each)

Stops one appliance · works offline. A floor sensor wired to motorized valves on one appliance's water lines. FloodStop's washer version closes both the hot and cold lines and sounds an alarm, with no Wi-Fi involved, and there are versions for water heaters.

Pluses: Stops the water at the source within seconds; No internet and nothing to hack; Covers the usual culprits: washers and water heaters.

Minuses: Protects one appliance only; Needs a plug-in adapter, and a reset after it trips; Won't help with a burst pipe or a toilet.

Best for: An old washer or water heater, or a home whose main valve is too stiff for a valve robot. If someone took it over: Nothing to take over, since it has no network connection.

### Valve robot on the main ($239–400)

Shuts off the whole home · works offline. A motor that clamps onto your existing quarter-turn main water valve and pairs with leak sensors around the home. YoLink's kit is $239 and fits valves from ½" to 2" in about 15 minutes; Elexa's Guardian kit is $400 with three sensors. The sensors close the valve directly, even when the internet is down.

Pluses: No plumber and no pipe cutting; Shuts off the whole home when any sensor gets wet; Works offline, with battery backup available; Easy to remove or move.

Minuses: Only fits lever-style ball valves, and an old, stiff valve may not turn; Only catches leaks where a sensor sits; Slow leaks inside walls go unseen; The app and alerts still need a hub and internet.

Best for: The best value for most homes. If someone took it over: At worst the water gets shut off, or someone unpairs sensors so a real leak goes unreported.

### Whole-home smart valve ($500–800+)

Watches water flow, tests for drips. Replaces the main shutoff and watches water flow and pressure. Moen Flo ($500 to $800 by pipe size) and Phyn Plus ($579) run a nightly test that briefly closes the supply and checks for a pressure drop, which catches slow leaks anywhere in the pipes. Flo's optional $5 a month plan covers up to $5,000 of an insurance deductible.

Pluses: Catches leaks anywhere, including inside walls and running toilets; Shuts off on its own when the flow looks like a burst pipe; Flo can still shut off if the Wi-Fi drops; Some insurers now discount premiums for one.

Minuses: A plumber has to fit it on the main pipe; Needs an outlet and has no battery, so add a small backup battery; False shutoffs while it learns; in one review a midday shower cut the water; Only works on 2.4 GHz Wi-Fi.

Best for: The strongest protection, set to Away mode when you travel. If someone took it over: At worst the water is shut off or alerts are silenced, so protect its login like a door lock's.

### Water use monitor (~$200)

Reads the meter · no shutoff. Flume straps onto the water meter, reads usage every minute, and alerts you to unusual flow, like water running while you're away. No plumbing, batteries last two to three years, no subscription.

Pluses: No plumbing, and it installs in minutes; Spots running toilets and irrigation leaks across the whole home; Away alerts when you travel.

Minuses: Can't shut anything off; Needs a standard, reachable water meter, which rules out wells and many apartments; Alerts need internet.

Best for: A cheap add-on to the Good or Better setup if your home has its own meter. If someone took it over: Someone could see your water use, which shows when you're away.

## Good, better, best

*12 · Pick a water setup*

### Good: Sensors and sirens

*From about $50 for a hub and four sensors, plus hoses and drip pans*

- Braided steel hoses on the washer, toilets, sinks and fridge
- Drip pans under the washer and water heater
- Smart leak sensors with sirens at the washer, water heater, dishwasher, fridge, toilets and sinks
- Alerts going to someone who can respond quickly
- Everyone at home knows where the main water shutoff is, and it turns

Catches: Leaks where you put sensors, as long as someone responds. Misses: Everything when nobody responds in time, plus hidden leaks in walls. It never stops the water.

### Better: Sensors that shut off the water

*About $239 to $400 for a valve robot kit, no plumber, on top of Good*

- Everything in Good
- A motor fitted to your existing main valve
- Sensors paired directly to it, so it closes even with the internet down
- Battery backup in the valve motor
- Appliance shutoffs on the washer or water heater if the main valve is old or stiff

Catches: Leaks where sensors sit, stopped within seconds, even offline. Misses: Slow leaks between sensors and inside walls, and a main valve too stiff to turn.

### Best: Whole-home monitoring

*$500 to $800 for the valve by pipe size, plus a plumber; optional $5 a month plan*

- A smart main valve, such as Moen Flo or Phyn Plus, with nightly drip tests
- Leak sensors linked to it
- A small backup battery for the valve
- Away mode when you travel, and a Home mode tuned so a long shower doesn't cut the water
- A call to your insurer about discounts

Catches: Leaks anywhere, including slow drips in walls and running toilets. Misses: Needs a plumber and power, can shut off by mistake while it learns, and needs checking against any well pump or pressure tank.

**On a well or rainwater catchment?** Meter monitors need a utility meter, so they're out. Whole-home valves can work, but have the installer check them against the pump and pressure tank first. **Insurance:** some insurers now discount premiums for an active shutoff device, so ask yours before buying.

## Tick it off: your action plan

### This week

- [ ] List every connected device, which app runs it, and who else can sign in. Include doorbells, cameras, thermostats, TVs and the router.
- [ ] Disconnect any appliance whose smart features you don't use.
- [ ] Give every account its own password and turn on two-step sign-in.
- [ ] Remove people who no longer need access: past housemates, installers, previous owners.
- [ ] Take anything that heats off smart plugs, and stop using recalled smart heaters.
- [ ] Replace off-brand streaming boxes with a major brand or the TV's own apps.
- [ ] Update every app, device and the router.

### This month

- [ ] Put smart devices on a separate Wi-Fi network from your phones and laptops; many routers call it a guest network.
- [ ] Change the router's admin password, and turn off remote admin and UPnP (a setting that lets devices open their own way in from the internet).
- [ ] Leak sensors at the washer, dishwasher, water heater and sinks, ideally tied to an automatic water shutoff.
- [ ] Braided steel hoses on the washer, toilets, sinks and fridge, and drip pans under the washer and water heater.
- [ ] A standalone fridge and freezer temperature alarm.
- [ ] Smoke, carbon monoxide and heat alarms that alert your phone.
- [ ] Choose alarms and valves with battery backup, so a power cut doesn't silence them.
- [ ] Reinforce outside door frames: four-screw strike plates with 3-inch screws.
- [ ] Ask your insurer, in writing, whether damage from a hacked device is covered.

### Retire

- [ ] Devices that no longer get updates and can't simply be disconnected.
- [ ] Anything on a recall list, including Govee and Atomi smart heaters.
- [ ] Off-brand streaming boxes, projectors and photo frames, especially "unlocked" ones.
- [ ] No-name smart plugs, bulbs, switches and fingerprint locks.

### Keep it up

- [ ] When someone no longer needs access, delete their code or account, and check it really stops working.
- [ ] Change the guest Wi-Fi password now and then.
- [ ] Check for updates and recalls a couple of times a year.
- [ ] Review who can sign in to each app.
- [ ] Look at the router's device list for anything you don't recognise.
- [ ] Check activity history for use while nobody was home.
- [ ] Test leak sensors and the shutoff valve, and swap weak batteries.

## Make it safe, then find out why

*14 · If a device acts on its own*

1. **Make it safe first.** Switch it off at the breaker or unplug it, and shut off the water if it's leaking.
2. **Read the history.** Check the app's activity log for commands nobody sent, and screenshot what you find.
3. **Lock the account.** Change the password, turn on two-step sign-in, and sign out every other session and user.
4. **Reset and rethink.** Factory reset, update, and only reconnect it if you need the smart features.
5. **Tell someone.** Report it to the maker, and keep the screenshots for your insurer.

## Seven questions before you buy

*15 · Before you buy the next one*

Unless a connected feature really earns its place, the plain model is often the safer buy.

- **Does it work fully with Wi-Fi off?** Good answer: Every cycle works from the buttons, with no app-only modes.
- **How many years of security updates are promised?** Good answer: A stated period, in writing. Miele's ten years is the benchmark; some brands promise two.
- **Does remote start need switching on at the machine every time?** Good answer: Yes, and opening the door cancels it.
- **Can it work locally, without the maker's servers?** Good answer: Look for Matter or Thread, newer standards that let devices work through a hub at home. Wemo's Thread devices kept working after Belkin shut its servers on January 31, 2026.
- **Does the maker publish security warnings?** Good answer: A public page of security notices, and a way to report flaws.
- **For streaming boxes: is it a major brand?** Good answer: Roku, Apple TV, Fire TV, Chromecast, or the TV's own apps.
- **Does it carry the U.S. Cyber Trust Mark?** Good answer: A new U.S. label for devices that meet basic security standards. It isn't widely on shelves yet; the FCC named ioXt to run it in April 2026, after UL Solutions withdrew.

### Plain-English glossary

- **Defrost cycle:** A routine pause in cooling that melts ice off a fridge's coils, normally for minutes, not hours.
- **Controller:** The small computer that runs a machine, like a store's fridges or your thermostat.
- **Firmware:** The built-in software that runs a device. Updates fix security holes.
- **End of support:** The maker has stopped fixing it. It may still work, but known holes stay open.
- **Maker's servers:** The company's online service. Most apps reach your device through it.
- **Two-step sign-in:** Logging in needs a second proof, usually a code sent to your phone.
- **Remote start:** Starting a machine from an app. Most major appliances need a button press first.
- **Separate network:** A second Wi-Fi just for smart devices, so they can't reach your phone and laptop.
- **Router admin password:** The password for your router's settings, separate from the Wi-Fi password.
- **UPnP:** A router setting that lets devices open their own way in from the internet. Safer off.
- **Matter, Thread:** Newer standards that let devices from different brands work together at home.
- **Botnet:** Thousands of hijacked devices controlled together.
- **Strike plate:** The metal plate in the door frame that the bolt slides into.

## Sources

- [Reuters via The Star: hackers heat French supermarket fridges](https://www.thestar.com.my/tech/tech-news/2026/10/12/french-supermarket-chain-intermarche-hit-by-cyberattack-150-stores-targeted)
- [BleepingComputer: refrigerators shut down (Predicta Lab and Shodan counts)](https://www.bleepingcomputer.com/news/security/cyberattack-shuts-down-refrigerators-at-french-supermarkets/)
- [The Record: refrigeration disrupted at hundreds of stores](https://therecord.media/cyberattack-disrupts-refridgeration-in-france)
- [CBC: Danfoss on outdated and end-of-life units](https://www.cbc.ca/news/business/france-fridge-hack-smart-devices-food-system-9.7379613)
- [Technology.org: Copeland and Dixell also hit](https://www.technology.org/2026/10/14/french-supermarket-fridge-hack-copeland-dixell-anssi/)
- [CERT-FR alert CERTFR-2026-ALE-012 (Oct 12, updated Oct 13 and Oct 16)](https://www.cert.cyber.gouv.fr/alerte/CERTFR-2026-ALE-012/)
- [SecurityWeek: attack widens to Copeland and Dixell](https://www.securityweek.com/supermarket-refrigeration-attack-widens-to-copeland-dixell-controllers/)
- [AP: about 700 of France's 10,000 supermarkets affected](https://apnews.com/article/france-cyberattack-supermarkets-refrigeration-systems-78a813a8efd466b360655339f96083dc)
- [The Guardian: who hacked France's supermarket fridges? (Oct 17)](https://www.theguardian.com/world/2026/oct/17/who-hacked-frances-supermarket-fridges)
- [Baptiste Robert (Predicta Lab): 2,752 Danfoss systems online](https://x.com/fs0c131y/status/2109693461800857775)
- [Claroty Team82: Danfoss controller research](https://claroty.com/team82/research/freeze-the-controller-defrost-the-food-uncovering-vulnerabilities-in-danfoss-refrigeration-controllers)
- [CISA advisory ICSA-25-140-03](https://www.cisa.gov/news-events/ics-advisories/icsa-25-140-03)
- [Intertek: UL 858 smart range requirements](https://cdn.intertek.com/www-intertek-com/dms-legacy/UL-858-SUN-Rev-4-18-2022-ED-4-18-2025-Amendment-1.pdf)
- [LG: washer remote control and door opening](https://www.lg.com/bd/support/product-help/CT40008239-20154476579716)
- [Check Point: HomeHack](https://blog.checkpoint.com/security/homehack-how-hackers-could-have-taken-control-of-lgs-iot-home-appliances/)
- [Consumer Reports: Atomi heater recall](https://www.consumerreports.org/appliances/appliance-recalls/atomi-space-heaters-recalled-for-fire-and-burn-hazards-a9581235556)
- [UPI: Govee heater recall](https://www.upi.com/Top_News/US/2024/11/08/Govee-space-heater-recall/4911731078927/)
- [BleepingComputer: FBI on BadBox 2.0](https://www.bleepingcomputer.com/news/security/fbi-badbox-20-android-malware-infects-millions-of-consumer-devices/)
- [Which?: smart appliance support periods](https://www.which.co.uk/policy-and-insight/article/smart-tvs-and-washing-machines-may-be-abandoned-by-brands-after-two-years-which-finds-av8Mv4T4BjPj)
- [ISPreview: cheap smart plug flaws](https://www.ispreview.co.uk/index.php/2021/05/security-researchers-find-vulnerabilities-in-uk-wifi-smart-plugs.html)
- [Jeff Geerling: Bosch cycles behind the cloud](https://www.jeffgeerling.com/blog/2025/i-wont-connect-my-dishwasher-your-stupid-cloud/)
- [Belkin: Wemo support ending](https://www.belkin.com/support/wemo)
- [Unsaflok: Saflok card lock research](https://unsaflok.com/)
- [NYT via Security Laboratories: Kaba Simplex magnet suit](https://www.securitylaboratories.org/wp-content/uploads/2020/05/Kaba-Faces-Suit-Over-Push-Button-Locks-Breached-With-Magnet-The-New-York-Times.pdf)
- [USENIX WOOT 2025: Master Lock smart lock flaws](https://www.usenix.org/system/files/woot25-diao.pdf)
- [Secura: smart lock and alarm flaws](https://secura.com/services/iot/consumer-products/security-concerns-in-popular-smart-home-devices)
- [St. Petersburg Police: burglary prevention](https://police.stpete.org/crimePreventionTips/residentialBurglaryPrevention.html)
- [ConsumerAffairs: water damage claim statistics (Triple-I data)](https://consumeraffairs.com/homeowners/water-damage-insurance-claims-statistics.html)
- [TechHive: Moen Flo review (archived)](https://web.archive.org/web/20260713040733/https://www.techhive.com/article/2333181/flo-smart-water-monitor-shutoff-review.html)
- [TechHive: Phyn Plus 2nd gen review (archived)](https://web.archive.org/web/20260713040848/https://www.techhive.com/article/1369351/phyn-plus-2nd-gen-smart-valve-review.html)
- [TechHive: Elexa Guardian leak prevention (archived)](https://web.archive.org/web/20230925140210/https://www.techhive.com/article/583111/elexa-guardian-leak-prevention-system.html)
- [Smart Home Compared: YoLink valve kit](https://smarthomecompared.com/water-shutoff-valves/yolink-valve-controller-2-with-evo-valve-operator)
- [Tech Enhanced Life: offline leak shutoff with YoLink](https://www.techenhancedlife.com/solutions/detect-water-leaks-shutoff-water-alert-me)
- [Android Central: Flume 2 review](https://www.androidcentral.com/flume-2-review)
- [Absolute Automation: FloodStop for washers](https://www.absoluteautomation.com/products/floodstop-fs34h90-for-washing-machines-3-4-water-line)
- [This Old House: best water leak detectors](https://www.thisoldhouse.com/shop/best-water-leak-detector)
- [Coverager: Stand and Moen insurance program](https://coverager.com/stand-and-moen-launch-smart-water-leak-program-with-insurance-discounts/)
- [FCC: ioXt named Cyber Trust Mark administrator](https://docs.fcc.gov/public/attachments/DOC-420764A1.txt)

---

Updated October 18, 2026. The entry path and attacker are still unconfirmed; figures are as reported, with sources named.

Made with Claude and AI collaborators at Superintelligent Silicon. Conceived by Wayne Goodwin.

## For agents

- Canonical URL: https://exploresuperintelligence.online/articles/defrost-mode/ (cite this page; this Markdown file is its plain-text companion)
- Cite as: *Defrost Mode*, Superintelligent Silicon (Explore Superintelligence), 2026-10-18, https://exploresuperintelligence.online/articles/defrost-mode/
- Licence: the text of this piece is CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); attribute Superintelligent Silicon and link https://exploresuperintelligence.online/articles/defrost-mode/. Illustrations, audio and fonts are not covered (illustrations and audio © Superintelligent Silicon, all rights reserved).
- Follow new books: https://exploresuperintelligence.online/feed.xml (RSS) or https://exploresuperintelligence.online/feed.json (JSON Feed). Email list, double opt-in, only with your human's explicit OK: https://exploresuperintelligence.online/agents.md#subscribe-api
- Support, optional and only with your human's explicit OK: tips $1 https://buy.stripe.com/fZu3cx4C845v2hW3fp5AQ00 · $3 https://buy.stripe.com/aFa4gBb0w1Xnf4I9DN5AQ01 · $5 https://buy.stripe.com/3cIaEZd8E0Tj9Ko8zJ5AQ02 (Stripe through Grok Ai Apps), or X Money to @GuyinGoldGlass where available.
- More: https://exploresuperintelligence.online/agents.md · https://exploresuperintelligence.online/llms.txt · exploresi@superintelligentsilicon.com

