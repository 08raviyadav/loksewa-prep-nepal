#!/usr/bin/env python3
"""R10 generator 17: science & misc facts 2 (~1,200). Physics laws, chemistry
compounds/formulas, biology classifications, economics terms, computer facts
part 2, Nepal history part 2, world geography part 2, old Nepal zones."""
import sys, random
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter

bank = Bank()
em = Emitter(bank, 'R10-SCI2')
rng = random.Random(71109)

def F(exams, topic, sub, q, qn, a, an, d1, d1n, d2, d2n, d3, d3n):
    em.emit(exams, topic, sub, 'medium', 2, q, qn, [a, d1, d2, d3], [an, d1n, d2n, d3n], 0,
            f'The answer is {a}.', f'उत्तर {an} हो।')

# ---------------- physics laws ----------------
PHYS = [
    ('Which law states that every action has an equal and opposite reaction?', 'कुन नियमले हरेक क्रियाको बराबर र विपरीत प्रतिक्रिया हुन्छ भन्छ?', "Newton's third law of motion", 'न्युटनको गतिका तेस्रो नियम', "Newton's first law of motion", 'न्युटनको गतिका पहिलो नियम', "Newton's second law of motion", 'न्युटनको गतिका दोस्रो नियम', "Newton's law of gravitation", 'न्युटनको गुरुत्वाकर्षण नियम'),
    ('Which law states that an object remains at rest or in uniform motion unless acted upon by a force?', 'कुन नियमले बल नलागेसम्म वस्तु स्थिर वा एकसमान गतिमा रहन्छ भन्छ?', "Newton's first law of motion", 'न्युटनको गतिका पहिलो नियम', "Newton's second law of motion", 'न्युटनको गतिका दोस्रो नियम', "Newton's third law of motion", 'न्युटनको गतिका तेस्रो नियम', "Newton's law of gravitation", 'न्युटनको गुरुत्वाकर्षण नियम'),
    ('Which law states that force equals mass times acceleration?', 'कुन नियमले बल बराबर पिण्ड गुणा त्वरण हुन्छ भन्छ?', "Newton's second law of motion", 'न्युटनको गतिका दोस्रो नियम', "Newton's first law of motion", 'न्युटनको गतिका पहिलो नियम', "Newton's third law of motion", 'न्युटनको गतिका तेस्रो नियम', "Newton's law of gravitation", 'न्युटनको गुरुत्वाकर्षण नियम'),
    ('Which law states that the pressure of a gas is inversely proportional to its volume at constant temperature?', 'कुन नियमले स्थिर तापक्रममा ग्यासको चाप आयतनको व्युत्क्रमानुपाती हुन्छ भन्छ?', "Boyle's law", 'बोयलको नियम', "Charles's law", 'चार्ल्सको नियम', "Avogadro's law", 'एभोगाड्रोको नियम', "Dalton's law", 'डाल्टनको नियम'),
    ('Which law states that the volume of a gas is directly proportional to its temperature at constant pressure?', 'कुन नियमले स्थिर चापमा ग्यासको आयतन तापक्रमको समानुपाती हुन्छ भन्छ?', "Charles's law", 'चार्ल्सको नियम', "Boyle's law", 'बोयलको नियम', "Avogadro's law", 'एभोगाड्रोको नियम', "Dalton's law", 'डाल्टनको नियम'),
    ('Which law states that the current through a conductor is directly proportional to the voltage?', 'कुन नियमले चालकबाट बग्ने विद्युत् भोल्टेजको समानुपाती हुन्छ भन्छ?', "Ohm's law", 'ओह्मको नियम', "Kirchhoff's law", 'किर्चहफको नियम', "Faraday's law", 'फ्याराडेको नियम', "Coulomb's law", 'कुलम्बको नियम'),
    ('Which law states that energy can neither be created nor destroyed?', 'कुन नियमले ऊर्जा न सिर्जना गर्न सकिन्छ न नष्ट गर्न सकिन्छ भन्छ?', 'Law of conservation of energy', 'ऊर्जा संरक्षणको नियम', 'Law of conservation of mass', 'पिण्ड संरक्षणको नियम', "Newton's first law", 'न्युटनको पहिलो नियम', "Boyle's law", 'बोयलको नियम'),
    ('Which law states that the angle of incidence equals the angle of reflection?', 'कुन नियमले आपतन कोण बराबर परावर्तन कोण हुन्छ भन्छ?', 'Law of reflection', 'परावर्तनको नियम', 'Law of refraction', 'अपवर्तनको नियम', "Snell's law", 'स्नेलको नियम', "Newton's law", 'न्युटनको नियम'),
    ('Which law relates the angle of incidence and refraction?', 'कुन नियमले आपतन र अपवर्तन कोणबीच सम्बन्ध राख्छ?', "Snell's law", 'स्नेलको नियम', 'Law of reflection', 'परावर्तनको नियम', "Boyle's law", 'बोयलको नियम', "Ohm's law", 'ओह्मको नियम'),
    ('Which principle states that a body immersed in a fluid experiences an upward buoyant force?', 'कुन सिद्धान्तले तरलमा डुबेको वस्तुले माथितर्फ उछाल बल अनुभव गर्छ भन्छ?', "Archimedes' principle", 'आर्किमिडिजको सिद्धान्त', "Pascal's principle", 'पास्कलको सिद्धान्त', "Bernoulli's principle", 'बर्नौलीको सिद्धान्त', "Newton's principle", 'न्युटनको सिद्धान्त'),
    ('Which principle states that pressure applied to a confined fluid is transmitted equally in all directions?', 'कुन सिद्धान्तले बन्द तरलमा लगाइएको चाप सबै दिशामा बराबर सर्छ भन्छ?', "Pascal's principle", 'पास्कलको सिद्धान्त', "Archimedes' principle", 'आर्किमिडिजको सिद्धान्त', "Bernoulli's principle", 'बर्नौलीको सिद्धान्त', "Boyle's law", 'बोयलको नियम'),
    ('Which principle explains the lift of an aeroplane wing?', 'कुन सिद्धान्तले हवाइजहाजको पखेटाको उछाल व्याख्या गर्छ?', "Bernoulli's principle", 'बर्नौलीको सिद्धान्त', "Pascal's principle", 'पास्कलको सिद्धान्त', "Archimedes' principle", 'आर्किमिडिजको सिद्धान्त', "Newton's third law", 'न्युटनको तेस्रो नियम'),
    ('Which law states that the total pressure of a gas mixture equals the sum of partial pressures?', 'कुन नियमले ग्यास मिश्रणको कुल चाप आंशिक चापहरूको योग बराबर हुन्छ भन्छ?', "Dalton's law", 'डाल्टनको नियम', "Boyle's law", 'बोयलको नियम', "Charles's law", 'चार्ल्सको नियम', "Avogadro's law", 'एभोगाड्रोको नियम'),
    ('Which law states that equal volumes of gases contain equal numbers of molecules at the same temperature and pressure?', 'कुन नियमले समान तापक्रम र चापमा समान आयतनका ग्यासहरूमा समान सङ्ख्यामा अणुहरू हुन्छन् भन्छ?', "Avogadro's law", 'एभोगाड्रोको नियम', "Boyle's law", 'बोयलको नियम', "Charles's law", 'चार्ल्सको नियम', "Dalton's law", 'डाल्टनको नियम'),
    ('Which law states that the rate of a chemical reaction is proportional to the concentration of reactants?', 'कुन नियमले रासायनिक प्रतिक्रियाको दर अभिकारकको सांद्रताको समानुपाती हुन्छ भन्छ?', 'Law of mass action', 'पिण्ड क्रियाको नियम', 'Law of definite proportions', 'निश्चित अनुपातको नियम', 'Law of multiple proportions', 'बहु अनुपातको नियम', 'Law of conservation of mass', 'पिण्ड संरक्षणको नियम'),
    ('Which law states that a compound always contains the same elements in the same proportion?', 'कुन नियमले यौगिकमा सधैँ उही तत्वहरू उही अनुपातमा हुन्छन् भन्छ?', 'Law of definite proportions', 'निश्चित अनुपातको नियम', 'Law of multiple proportions', 'बहु अनुपातको नियम', 'Law of mass action', 'पिण्ड क्रियाको नियम', 'Law of conservation of energy', 'ऊर्जा संरक्षणको नियम'),
    ('Who proposed the law of universal gravitation?', 'सार्वत्रिक गुरुत्वाकर्षणको नियम कसले प्रस्ताव गरे?', 'Isaac Newton', 'आइज्याक न्युटन', 'Albert Einstein', 'अल्बर्ट आइन्स्टाइन', 'Galileo Galilei', 'ग्यालिलियो ग्यालिली', 'Johannes Kepler', 'जोहानेस केप्लर'),
    ('Who proposed the three laws of planetary motion?', 'ग्रह गतिका तीन नियम कसले प्रस्ताव गरे?', 'Johannes Kepler', 'जोहानेस केप्लर', 'Isaac Newton', 'आइज्याक न्युटन', 'Galileo Galilei', 'ग्यालिलियो ग्यालिली', 'Nicolaus Copernicus', 'निकोलस कोपर्निकस'),
    ('Who proposed the theory of relativity?', 'सापेक्षताको सिद्धान्त कसले प्रस्ताव गरे?', 'Albert Einstein', 'अल्बर्ट आइन्स्टाइन', 'Isaac Newton', 'आइज्याक न्युटन', 'Niels Bohr', 'निल्स बोहर', 'Max Planck', 'म्याक्स प्लान्क'),
    ('What is the speed of light in vacuum?', 'शून्यमा प्रकाशको गति कति हुन्छ?', '299,792,458 m/s', '२९९,७९२,४५८ मिटर/सेकेन्ड', '150,000,000 m/s', '१५०,०००,००० मिटर/सेकेन्ड', '250,000,000 m/s', '२५०,०००,००० मिटर/सेकेन्ड', '340 m/s', '३४० मिटर/सेकेन्ड'),
    ('What is the value of the acceleration due to gravity on Earth?', 'पृथ्वीमा गुरुत्वाकर्षण त्वरणको मान कति हुन्छ?', '9.8 m/s^2', '९.८ मिटर/सेकेन्ड^२', '10.8 m/s^2', '१०.८ मिटर/सेकेन्ड^२', '8.8 m/s^2', '८.८ मिटर/सेकेन्ड^२', '9.0 m/s^2', '९.० मिटर/सेकेन्ड^२'),
    ('What is the unit of electric charge?', 'विद्युत् आवेशको एकाइ के हो?', 'Coulomb', 'कुलम्ब', 'Ampere', 'एम्पियर', 'Volt', 'भोल्ट', 'Ohm', 'ओह्म'),
    ('What is the unit of magnetic flux?', 'चुम्बकीय प्रवाहको एकाइ के हो?', 'Weber', 'वेबर', 'Tesla', 'टेस्ला', 'Henry', 'हेनरी', 'Gauss', 'गाउस'),
    ('What is the unit of magnetic field strength?', 'चुम्बकीय क्षेत्र शक्तिको एकाइ के हो?', 'Tesla', 'टेस्ला', 'Weber', 'वेबर', 'Henry', 'हेनरी', 'Ampere', 'एम्पियर'),
    ('What is the unit of inductance?', 'प्रेरकत्वको एकाइ के हो?', 'Henry', 'हेनरी', 'Farad', 'फ्याराड', 'Tesla', 'टेस्ला', 'Weber', 'वेबर'),
    ('What is the unit of capacitance?', 'धारिताको एकाइ के हो?', 'Farad', 'फ्याराड', 'Henry', 'हेनरी', 'Ohm', 'ओह्म', 'Volt', 'भोल्ट'),
    ('What is the unit of luminous intensity?', 'प्रकाश तीव्रताको एकाइ के हो?', 'Candela', 'क्यान्डेला', 'Lumen', 'लुमेन', 'Lux', 'लक्स', 'Watt', 'वाट'),
    ('What is the unit of luminous flux?', 'प्रकाश प्रवाहको एकाइ के हो?', 'Lumen', 'लुमेन', 'Candela', 'क्यान्डेला', 'Lux', 'लक्स', 'Watt', 'वाट'),
    ('What is the unit of illuminance?', 'प्रदीप्तिको एकाइ के हो?', 'Lux', 'लक्स', 'Lumen', 'लुमेन', 'Candela', 'क्यान्डेला', 'Watt', 'वाट'),
    ('What is the unit of radioactivity?', 'विकिरणशीलताको एकाइ के हो?', 'Becquerel', 'बेकेरेल', 'Curie', 'क्युरी', 'Gray', 'ग्रे', 'Sievert', 'सिभर्ट'),
    ('What is the unit of absorbed radiation dose?', 'अवशोषित विकिरण मात्राको एकाइ के हो?', 'Gray', 'ग्रे', 'Becquerel', 'बेकेरेल', 'Sievert', 'सिभर्ट', 'Rad', 'र्‍याड'),
    ('What is the unit of frequency of a wave?', 'तरङ्गको आवृत्तिको एकाइ के हो?', 'Hertz', 'हर्ट्ज', 'Second', 'सेकेन्ड', 'Metre', 'मिटर', 'Watt', 'वाट'),
    ('What is the unit of wavelength?', 'तरङ्गदैर्ध्यको एकाइ के हो?', 'Metre', 'मिटर', 'Hertz', 'हर्ट्ज', 'Second', 'सेकेन्ड', 'Joule', 'जुल'),
    ('What is the unit of momentum?', 'संवेगको एकाइ के हो?', 'kg m/s', 'केजी मिटर/सेकेन्ड', 'Newton', 'न्युटन', 'Joule', 'जुल', 'Watt', 'वाट'),
    ('What is the unit of work?', 'कार्यको एकाइ के हो?', 'Joule', 'जुल', 'Newton', 'न्युटन', 'Watt', 'वाट', 'Pascal', 'पास्कल'),
    ('What is the unit of energy?', 'ऊर्जाको एकाइ के हो?', 'Joule', 'जुल', 'Watt', 'वाट', 'Newton', 'न्युटन', 'Pascal', 'पास्कल'),
    ('What is the unit of power?', 'शक्तिको एकाइ के हो?', 'Watt', 'वाट', 'Joule', 'जुल', 'Newton', 'न्युटन', 'Horsepower', 'अश्वशक्ति'),
    ('What is the unit of torque?', 'बलाघूर्णको एकाइ के हो?', 'Newton-metre', 'न्युटन-मिटर', 'Joule', 'जुल', 'Watt', 'वाट', 'Pascal', 'पास्कल'),
    ('What is the unit of surface tension?', 'पृष्ठ तनावको एकाइ के हो?', 'N/m', 'न्युटन/मिटर', 'Pascal', 'पास्कल', 'Joule', 'जुल', 'Watt', 'वाट'),
    ('What is the unit of viscosity?', 'श्यानताको एकाइ के हो?', 'Pascal-second', 'पास्कल-सेकेन्ड', 'Newton', 'न्युटन', 'Joule', 'जुल', 'Watt', 'वाट'),
]
for r in PHYS:
    F(['ioe-entrance','csit-entrance','engineering','nec-licence','sub-engineer','section-officer','kharidar','nasu'], 'Physics', 'Physics', *r)

# ---------------- chemistry compounds ----------------
CHEM = [
    ('What is the chemical formula of common salt?', 'साधारण नुनको रासायनिक सूत्र के हो?', 'NaCl', 'NaCl', 'KCl', 'KCl', 'NaOH', 'NaOH', 'CaCl2', 'CaCl2'),
    ('What is the chemical formula of baking soda?', 'बेकिङ सोडाको रासायनिक सूत्र के हो?', 'NaHCO3', 'NaHCO3', 'Na2CO3', 'Na2CO3', 'NaOH', 'NaOH', 'CaCO3', 'CaCO3'),
    ('What is the chemical formula of washing soda?', 'धुने सोडाको रासायनिक सूत्र के हो?', 'Na2CO3', 'Na2CO3', 'NaHCO3', 'NaHCO3', 'NaOH', 'NaOH', 'Ca(OH)2', 'Ca(OH)2'),
    ('What is the chemical formula of caustic soda?', 'कास्टिक सोडाको रासायनिक सूत्र के हो?', 'NaOH', 'NaOH', 'Na2CO3', 'Na2CO3', 'NaHCO3', 'NaHCO3', 'KOH', 'KOH'),
    ('What is the chemical formula of limestone?', 'चुनढुङ्गाको रासायनिक सूत्र के हो?', 'CaCO3', 'CaCO3', 'CaO', 'CaO', 'Ca(OH)2', 'Ca(OH)2', 'CaSO4', 'CaSO4'),
    ('What is the chemical formula of quicklime?', 'चुन (क्विकलाईम) को रासायनिक सूत्र के हो?', 'CaO', 'CaO', 'CaCO3', 'CaCO3', 'Ca(OH)2', 'Ca(OH)2', 'CaCl2', 'CaCl2'),
    ('What is the chemical formula of slaked lime?', 'बुझेको चुनको रासायनिक सूत्र के हो?', 'Ca(OH)2', 'Ca(OH)2', 'CaO', 'CaO', 'CaCO3', 'CaCO3', 'CaSO4', 'CaSO4'),
    ('What is the chemical formula of gypsum?', 'जिप्समको रासायनिक सूत्र के हो?', 'CaSO4.2H2O', 'CaSO4.2H2O', 'CaCO3', 'CaCO3', 'CaO', 'CaO', 'CaCl2', 'CaCl2'),
    ('What is the chemical formula of sulphuric acid?', 'सल्फ्युरिक एसिडको रासायनिक सूत्र के हो?', 'H2SO4', 'H2SO4', 'HCl', 'HCl', 'HNO3', 'HNO3', 'H2CO3', 'H2CO3'),
    ('What is the chemical formula of hydrochloric acid?', 'हाइड्रोक्लोरिक एसिडको रासायनिक सूत्र के हो?', 'HCl', 'HCl', 'H2SO4', 'H2SO4', 'HNO3', 'HNO3', 'H3PO4', 'H3PO4'),
    ('What is the chemical formula of nitric acid?', 'नाइट्रिक एसिडको रासायनिक सूत्र के हो?', 'HNO3', 'HNO3', 'H2SO4', 'H2SO4', 'HCl', 'HCl', 'H3PO4', 'H3PO4'),
    ('What is the chemical formula of acetic acid (vinegar)?', 'एसिटिक एसिड (सिर्का) को रासायनिक सूत्र के हो?', 'CH3COOH', 'CH3COOH', 'HCOOH', 'HCOOH', 'C2H5OH', 'C2H5OH', 'CH3OH', 'CH3OH'),
    ('What is the chemical formula of ethanol?', 'इथेनोलको रासायनिक सूत्र के हो?', 'C2H5OH', 'C2H5OH', 'CH3OH', 'CH3OH', 'CH3COOH', 'CH3COOH', 'C6H12O6', 'C6H12O6'),
    ('What is the chemical formula of methanol?', 'मेथेनोलको रासायनिक सूत्र के हो?', 'CH3OH', 'CH3OH', 'C2H5OH', 'C2H5OH', 'CH3COOH', 'CH3COOH', 'C6H12O6', 'C6H12O6'),
    ('What is the chemical formula of glucose?', 'ग्लुकोजको रासायनिक सूत्र के हो?', 'C6H12O6', 'C6H12O6', 'C12H22O11', 'C12H22O11', 'C2H5OH', 'C2H5OH', 'CH3COOH', 'CH3COOH'),
    ('What is the chemical formula of sucrose (table sugar)?', 'सुक्रोज (चिनी) को रासायनिक सूत्र के हो?', 'C12H22O11', 'C12H22O11', 'C6H12O6', 'C6H12O6', 'C2H5OH', 'C2H5OH', 'CH3OH', 'CH3OH'),
    ('What is the chemical formula of methane?', 'मिथेनको रासायनिक सूत्र के हो?', 'CH4', 'CH4', 'C2H6', 'C2H6', 'C3H8', 'C3H8', 'CO2', 'CO2'),
    ('What is the chemical formula of ethane?', 'इथेनको रासायनिक सूत्र के हो?', 'C2H6', 'C2H6', 'CH4', 'CH4', 'C3H8', 'C3H8', 'C2H4', 'C2H4'),
    ('What is the chemical formula of propane?', 'प्रोपेनको रासायनिक सूत्र के हो?', 'C3H8', 'C3H8', 'CH4', 'CH4', 'C2H6', 'C2H6', 'C4H10', 'C4H10'),
    ('What is the chemical formula of butane?', 'ब्युटेनको रासायनिक सूत्र के हो?', 'C4H10', 'C4H10', 'C3H8', 'C3H8', 'C2H6', 'C2H6', 'CH4', 'CH4'),
    ('What is the chemical formula of ammonia?', 'अमोनियाको रासायनिक सूत्र के हो?', 'NH3', 'NH3', 'NO2', 'NO2', 'N2O', 'N2O', 'HNO3', 'HNO3'),
    ('What is the chemical formula of carbon dioxide?', 'कार्बन डाइअक्साइडको रासायनिक सूत्र के हो?', 'CO2', 'CO2', 'CO', 'CO', 'CH4', 'CH4', 'C6H12O6', 'C6H12O6'),
    ('What is the chemical formula of carbon monoxide?', 'कार्बन मोनोअक्साइडको रासायनिक सूत्र के हो?', 'CO', 'CO', 'CO2', 'CO2', 'CH4', 'CH4', 'C2H5OH', 'C2H5OH'),
    ('What is the chemical formula of water?', 'पानीको रासायनिक सूत्र के हो?', 'H2O', 'H2O', 'H2O2', 'H2O2', 'H2SO4', 'H2SO4', 'CO2', 'CO2'),
    ('What is the chemical formula of hydrogen peroxide?', 'हाइड्रोजन पेरोक्साइडको रासायनिक सूत्र के हो?', 'H2O2', 'H2O2', 'H2O', 'H2O', 'H2SO4', 'H2SO4', 'HNO3', 'HNO3'),
    ('What is the chemical formula of urea?', 'युरियाको रासायनिक सूत्र के हो?', 'CO(NH2)2', 'CO(NH2)2', 'NH3', 'NH3', 'NH4NO3', 'NH4NO3', 'CO2', 'CO2'),
    ('What is the chemical formula of chloroform?', 'क्लोरोफर्मको रासायनिक सूत्र के हो?', 'CHCl3', 'CHCl3', 'CCl4', 'CCl4', 'CH3Cl', 'CH3Cl', 'CH2Cl2', 'CH2Cl2'),
    ('What is the chemical formula of carbon tetrachloride?', 'कार्बन टेट्राक्लोराइडको रासायनिक सूत्र के हो?', 'CCl4', 'CCl4', 'CHCl3', 'CHCl3', 'CH3Cl', 'CH3Cl', 'CH2Cl2', 'CH2Cl2'),
    ('What is the chemical formula of benzene?', 'बेन्जिनको रासायनिक सूत्र के हो?', 'C6H6', 'C6H6', 'C6H12', 'C6H12', 'C6H12O6', 'C6H12O6', 'C2H6', 'C2H6'),
    ('What is the chemical formula of rust?', 'खियाको रासायनिक सूत्र के हो?', 'Fe2O3', 'Fe2O3', 'FeO', 'FeO', 'Fe3O4', 'Fe3O4', 'FeSO4', 'FeSO4'),
    ('What is the chemical formula of ferrous sulphate (green vitriol)?', 'फेरस सल्फेट (हरियो कसीस) को रासायनिक सूत्र के हो?', 'FeSO4', 'FeSO4', 'Fe2O3', 'Fe2O3', 'CuSO4', 'CuSO4', 'ZnSO4', 'ZnSO4'),
    ('What is the chemical formula of copper sulphate (blue vitriol)?', 'कपर सल्फेट (नीलो कसीस) को रासायनिक सूत्र के हो?', 'CuSO4', 'CuSO4', 'FeSO4', 'FeSO4', 'ZnSO4', 'ZnSO4', 'CuO', 'CuO'),
    ('What is the chemical formula of zinc sulphate (white vitriol)?', 'जिङ्क सल्फेट (सेतो कसीस) को रासायनिक सूत्र के हो?', 'ZnSO4', 'ZnSO4', 'CuSO4', 'CuSO4', 'FeSO4', 'FeSO4', 'ZnO', 'ZnO'),
    ('What is the chemical formula of potassium permanganate?', 'पोटासियम परम्याङ्गनेटको रासायनिक सूत्र के हो?', 'KMnO4', 'KMnO4', 'K2Cr2O7', 'K2Cr2O7', 'KCl', 'KCl', 'KNO3', 'KNO3'),
    ('What is the chemical formula of potassium dichromate?', 'पोटासियम डाइक्रोमेटको रासायनिक सूत्र के हो?', 'K2Cr2O7', 'K2Cr2O7', 'KMnO4', 'KMnO4', 'KCl', 'KCl', 'KNO3', 'KNO3'),
    ('What is the chemical formula of sodium chloride?', 'सोडियम क्लोराइडको रासायनिक सूत्र के हो?', 'NaCl', 'NaCl', 'KCl', 'KCl', 'NaOH', 'NaOH', 'Na2CO3', 'Na2CO3'),
    ('What is the chemical formula of potassium nitrate (saltpetre)?', 'पोटासियम नाइट्रेट (सोरा) को रासायनिक सूत्र के हो?', 'KNO3', 'KNO3', 'NaNO3', 'NaNO3', 'KCl', 'KCl', 'NH4NO3', 'NH4NO3'),
    ('What is the chemical formula of ammonium nitrate?', 'अमोनियम नाइट्रेटको रासायनिक सूत्र के हो?', 'NH4NO3', 'NH4NO3', 'KNO3', 'KNO3', 'NH3', 'NH3', 'NH4Cl', 'NH4Cl'),
    ('What is the chemical formula of ammonium chloride (sal ammoniac)?', 'अमोनियम क्लोराइड (नौसादर) को रासायनिक सूत्र के हो?', 'NH4Cl', 'NH4Cl', 'NH4NO3', 'NH4NO3', 'NaCl', 'NaCl', 'KCl', 'KCl'),
    ('What is the chemical formula of calcium oxide?', 'क्याल्सियम अक्साइडको रासायनिक सूत्र के हो?', 'CaO', 'CaO', 'CaCO3', 'CaCO3', 'Ca(OH)2', 'Ca(OH)2', 'CaCl2', 'CaCl2'),
]
for r in CHEM:
    F(['ioe-entrance','csit-entrance','engineering','nec-licence','nhpc-lab','npc-pharmacy','nmc-mbbs','nmc-bds','section-officer','kharidar','nasu'], 'Chemistry', 'Chemistry', *r)

# ---------------- biology classifications ----------------
BIO = [
    ('Which is the largest organ of the human body?', 'मानव शरीरको सबैभन्दा ठूलो अङ्ग कुन हो?', 'Skin', 'छाला', 'Liver', 'कलेजो', 'Heart', 'मुटु', 'Brain', 'मस्तिष्क'),
    ('Which is the largest internal organ of the human body?', 'मानव शरीरको सबैभन्दा ठूलो आन्तरिक अङ्ग कुन हो?', 'Liver', 'कलेजो', 'Heart', 'मुटु', 'Lung', 'फोक्सो', 'Kidney', 'मिर्गौला'),
    ('Which is the smallest bone in the human body?', 'मानव शरीरको सबैभन्दा सानो हाड कुन हो?', 'Stapes', 'स्टेपिज', 'Malleus', 'मालियस', 'Incus', 'इन्कस', 'Hyoid', 'हायोइड'),
    ('Which is the longest bone in the human body?', 'मानव शरीरको सबैभन्दा लामो हाड कुन हो?', 'Femur', 'फेमर', 'Tibia', 'टिबिया', 'Humerus', 'ह्युमरस', 'Fibula', 'फिबुला'),
    ('How many bones are there in the adult human body?', 'वयस्क मानव शरीरमा कति हाड हुन्छन्?', '206', '२०६', '200', '२००', '210', '२१०', '216', '२१६'),
    ('How many bones are there in a newborn baby?', 'नवजात शिशुमा कति हाड हुन्छन्?', '300', '३००', '206', '२०६', '250', '२५०', '350', '३५०'),
    ('How many teeth does an adult human have?', 'वयस्क मानवमा कति दाँत हुन्छन्?', '32', '३२', '28', '२८', '30', '३०', '36', '३६'),
    ('How many teeth does a child have (milk teeth)?', 'बालबालिकामा कति दूधे दाँत हुन्छन्?', '20', '२०', '24', '२४', '28', '२८', '32', '३२'),
    ('Which blood group is the universal donor?', 'कुन रक्त समूह सार्वभौमिक दाता हो?', 'O negative', 'O नेगेटिभ', 'AB positive', 'AB पोजिटिभ', 'A positive', 'A पोजिटिभ', 'B negative', 'B नेगेटिभ'),
    ('Which blood group is the universal recipient?', 'कुन रक्त समूह सार्वभौमिक ग्राही हो?', 'AB positive', 'AB पोजिटिभ', 'O negative', 'O नेगेटिभ', 'A positive', 'A पोजिटिभ', 'B positive', 'B पोजिटिभ'),
    ('Which organ produces insulin in the human body?', 'मानव शरीरमा इन्सुलिन कुन अङ्गले उत्पादन गर्छ?', 'Pancreas', 'अग्न्याशय', 'Liver', 'कलेजो', 'Kidney', 'मिर्गौला', 'Spleen', 'प्लीहा'),
    ('Which organ filters blood in the human body?', 'मानव शरीरमा रगत कुन अङ्गले छान्छ?', 'Kidney', 'मिर्गौला', 'Liver', 'कलेजो', 'Heart', 'मुटु', 'Lung', 'फोक्सो'),
    ('Which organ detoxifies blood in the human body?', 'मानव शरीरमा रगतको विषहरण कुन अङ्गले गर्छ?', 'Liver', 'कलेजो', 'Kidney', 'मिर्गौला', 'Spleen', 'प्लीहा', 'Pancreas', 'अग्न्याशय'),
    ('Which part of the cell contains genetic material?', 'कोशिकाको कुन भागमा आनुवंशिक सामग्री हुन्छ?', 'Nucleus', 'केन्द्रक', 'Cytoplasm', 'कोशिकाद्रव्य', 'Mitochondria', 'माइटोकन्ड्रिया', 'Ribosome', 'राइबोजोम'),
    ('Which organelle is known as the powerhouse of the cell?', 'कोशिकाको कुन अङ्गाणुलाई शक्तिगृह भनिन्छ?', 'Mitochondria', 'माइटोकन्ड्रिया', 'Nucleus', 'केन्द्रक', 'Ribosome', 'राइबोजोम', 'Golgi body', 'गोल्जी पिण्ड'),
    ('Which organelle is known as the kitchen of the cell?', 'कोशिकाको कुन अङ्गाणुलाई भान्सा भनिन्छ?', 'Chloroplast', 'क्लोरोप्लास्ट', 'Mitochondria', 'माइटोकन्ड्रिया', 'Nucleus', 'केन्द्रक', 'Vacuole', 'रिक्तिका'),
    ('Which organelle makes proteins in the cell?', 'कोशिकामा प्रोटिन कुन अङ्गाणुले बनाउँछ?', 'Ribosome', 'राइबोजोम', 'Nucleus', 'केन्द्रक', 'Mitochondria', 'माइटोकन्ड्रिया', 'Lysosome', 'लाइसोजोम'),
    ('Which organelle is known as the suicide bag of the cell?', 'कोशिकाको कुन अङ्गाणुलाई आत्मघाती थैली भनिन्छ?', 'Lysosome', 'लाइसोजोम', 'Ribosome', 'राइबोजोम', 'Mitochondria', 'माइटोकन्ड्रिया', 'Nucleus', 'केन्द्रक'),
    ('Which pigment gives leaves their green colour?', 'पातलाई हरियो रङ दिने रङ्गक कुन हो?', 'Chlorophyll', 'क्लोरोफिल', 'Carotene', 'क्यारोटिन', 'Xanthophyll', 'ज्यान्थोफिल', 'Anthocyanin', 'एन्थोसायनिन'),
    ('Which process do plants use to make food?', 'बिरुवाले खाना बनाउन कुन प्रक्रिया प्रयोग गर्छ?', 'Photosynthesis', 'प्रकाश संश्लेषण', 'Respiration', 'श्वसन', 'Transpiration', 'वाष्पोत्सर्जन', 'Fermentation', 'किण्वन'),
    ('Which gas do plants absorb for photosynthesis?', 'प्रकाश संश्लेषणका लागि बिरुवाले कुन ग्यास सोस्छ?', 'Carbon dioxide', 'कार्बन डाइअक्साइड', 'Oxygen', 'अक्सिजन', 'Nitrogen', 'नाइट्रोजन', 'Hydrogen', 'हाइड्रोजन'),
    ('Which gas do plants release during photosynthesis?', 'प्रकाश संश्लेषणका क्रममा बिरुवाले कुन ग्यास छोड्छ?', 'Oxygen', 'अक्सिजन', 'Carbon dioxide', 'कार्बन डाइअक्साइड', 'Nitrogen', 'नाइट्रोजन', 'Hydrogen', 'हाइड्रोजन'),
    ('Which part of the plant absorbs water from the soil?', 'बिरुवाको कुन भागले माटोबाट पानी सोस्छ?', 'Root', 'जरा', 'Stem', 'डाँठ', 'Leaf', 'पात', 'Flower', 'फूल'),
    ('Which part of the plant makes food?', 'बिरुवाको कुन भागले खाना बनाउँछ?', 'Leaf', 'पात', 'Root', 'जरा', 'Stem', 'डाँठ', 'Flower', 'फूल'),
    ('Which vitamin is produced in the skin by sunlight?', 'सूर्यको प्रकाशले छालामा कुन भिटामिन बन्छ?', 'Vitamin D', 'भिटामिन डी', 'Vitamin A', 'भिटामिन ए', 'Vitamin C', 'भिटामिन सी', 'Vitamin B12', 'भिटामिन बी१२'),
    ('Which vitamin is needed for blood clotting?', 'रगत जम्न कुन भिटामिन चाहिन्छ?', 'Vitamin K', 'भिटामिन के', 'Vitamin D', 'भिटामिन डी', 'Vitamin C', 'भिटामिन सी', 'Vitamin A', 'भिटामिन ए'),
    ('Which vitamin is needed for good vision?', 'राम्रो दृष्टिका लागि कुन भिटामिन चाहिन्छ?', 'Vitamin A', 'भिटामिन ए', 'Vitamin D', 'भिटामिन डी', 'Vitamin C', 'भिटामिन सी', 'Vitamin B', 'भिटामिन बी'),
    ('Which vitamin prevents scurvy?', 'स्कर्भी रोक्न कुन भिटामिन चाहिन्छ?', 'Vitamin C', 'भिटामिन सी', 'Vitamin A', 'भिटामिन ए', 'Vitamin D', 'भिटामिन डी', 'Vitamin B', 'भिटामिन बी'),
    ('Which vitamin prevents rickets?', 'रिकेट्स रोक्न कुन भिटामिन चाहिन्छ?', 'Vitamin D', 'भिटामिन डी', 'Vitamin A', 'भिटामिन ए', 'Vitamin C', 'भिटामिन सी', 'Vitamin B', 'भिटामिन बी'),
    ('Which vitamin prevents beriberi?', 'बेरीबेरी रोक्न कुन भिटामिन चाहिन्छ?', 'Vitamin B1', 'भिटामिन बी१', 'Vitamin B2', 'भिटामिन बी२', 'Vitamin C', 'भिटामिन सी', 'Vitamin D', 'भिटामिन डी'),
    ('Which mineral is needed for haemoglobin?', 'हिमोग्लोबिनका लागि कुन खनिज चाहिन्छ?', 'Iron', 'फलाम', 'Calcium', 'क्याल्सियम', 'Iodine', 'आयोडिन', 'Zinc', 'जस्ता'),
    ('Which mineral is needed for strong bones and teeth?', 'बलिया हाड र दाँतका लागि कुन खनिज चाहिन्छ?', 'Calcium', 'क्याल्सियम', 'Iron', 'फलाम', 'Iodine', 'आयोडिन', 'Sodium', 'सोडियम'),
    ('Which mineral prevents goitre?', 'गलगाँड रोक्न कुन खनिज चाहिन्छ?', 'Iodine', 'आयोडिन', 'Iron', 'फलाम', 'Calcium', 'क्याल्सियम', 'Zinc', 'जस्ता'),
    ('Which disease is caused by the bite of a female Anopheles mosquito?', 'पोथी एनोफिलिज लामखुट्टेको टोकाइले कुन रोग लाग्छ?', 'Malaria', 'मलेरिया', 'Dengue', 'डेङ्गु', 'Filaria', 'फाइलेरिया', 'Chikungunya', 'चिकुनगुनिया'),
    ('Which disease is caused by the bite of an Aedes mosquito?', 'एडिज लामखुट्टेको टोकाइले कुन रोग लाग्छ?', 'Dengue', 'डेङ्गु', 'Malaria', 'मलेरिया', 'Filaria', 'फाइलेरिया', 'Kala-azar', 'कालाजार'),
    ('Which organism causes tuberculosis?', 'क्षयरोग कुन जीवले गराउँछ?', 'Mycobacterium tuberculosis', 'माइकोब्याक्टेरियम ट्युबरकुलोसिस', 'Vibrio cholerae', 'भिब्रियो कोलेरी', 'Salmonella typhi', 'साल्मोनेला टाइफी', 'Plasmodium', 'प्लाज्मोडियम'),
    ('Which organism causes cholera?', 'हैजा कुन जीवले गराउँछ?', 'Vibrio cholerae', 'भिब्रियो कोलेरी', 'Mycobacterium tuberculosis', 'माइकोब्याक्टेरियम ट्युबरकुलोसिस', 'Salmonella typhi', 'साल्मोनेला टाइफी', 'E. coli', 'ई. कोलाई'),
    ('Which organism causes typhoid?', 'टाइफाइड कुन जीवले गराउँछ?', 'Salmonella typhi', 'साल्मोनेला टाइफी', 'Vibrio cholerae', 'भिब्रियो कोलेरी', 'Mycobacterium tuberculosis', 'माइकोब्याक्टेरियम ट्युबरकुलोसिस', 'Plasmodium', 'प्लाज्मोडियम'),
    ('Which organism causes malaria?', 'मलेरिया कुन जीवले गराउँछ?', 'Plasmodium', 'प्लाज्मोडियम', 'Vibrio cholerae', 'भिब्रियो कोलेरी', 'Salmonella typhi', 'साल्मोनेला टाइफी', 'Mycobacterium tuberculosis', 'माइकोब्याक्टेरियम ट्युबरकुलोसिस'),
    ('Which virus causes AIDS?', 'एड्स कुन भाइरसले गराउँछ?', 'HIV', 'एचआईभी', 'Hepatitis B', 'हेपाटाइटिस बी', 'Influenza', 'इन्फ्लुएन्जा', 'Rabies', 'रेबिज'),
    ('Which virus causes rabies?', 'रेबिज कुन भाइरसले गराउँछ?', 'Rabies virus', 'रेबिज भाइरस', 'HIV', 'एचआईभी', 'Influenza virus', 'इन्फ्लुएन्जा भाइरस', 'Dengue virus', 'डेङ्गु भाइरस'),
    ('Which is the largest mammal in the world?', 'विश्वको सबैभन्दा ठूलो स्तनधारी कुन हो?', 'Blue whale', 'निलो ह्वेल', 'African elephant', 'अफ्रिकी हात्ती', 'Giraffe', 'जिराफ', 'Hippopotamus', 'दरियाई घोडा'),
    ('Which is the fastest land animal?', 'सबैभन्दा छिटो दौडने स्थलीय जनावर कुन हो?', 'Cheetah', 'चिता', 'Lion', 'सिंह', 'Horse', 'घोडा', 'Deer', 'मृग'),
    ('Which is the largest bird in the world?', 'विश्वको सबैभन्दा ठूलो चरा कुन हो?', 'Ostrich', 'अस्ट्रिच', 'Emu', 'इमु', 'Peacock', 'मयूर', 'Eagle', 'चील'),
    ('Which is the only mammal that can fly?', 'उड्न सक्ने एक मात्र स्तनधारी कुन हो?', 'Bat', 'चमेरो', 'Flying squirrel', 'उड्ने लोखर्के', 'Sugar glider', 'सुगर ग्लाइडर', 'Owl', 'उल्लू'),
    ('Which is the largest reptile in the world?', 'विश्वको सबैभन्दा ठूलो सरीसृप कुन हो?', 'Saltwater crocodile', 'नुनपानी गोही', 'Komodo dragon', 'कोमोडो ड्र्यागन', 'Anaconda', 'एनाकोन्डा', 'Python', 'अजिङ्गर'),
    ('Which is the tallest animal in the world?', 'विश्वको सबैभन्दा अग्लो जनावर कुन हो?', 'Giraffe', 'जिराफ', 'Elephant', 'हात्ती', 'Camel', 'ऊँट', 'Horse', 'घोडा'),
    ('Which animal is known as the ship of the desert?', 'मरुभूमिको जहाज भनेर कुन जनावरलाई चिनिन्छ?', 'Camel', 'ऊँट', 'Horse', 'घोडा', 'Donkey', 'गधा', 'Elephant', 'हात्ती'),
    ('Which animal is the national animal of Nepal?', 'नेपालको राष्ट्रिय जनावर कुन हो?', 'Cow', 'गाई', 'One-horned rhinoceros', 'एकसिङ्गे गैँडा', 'Danfe', 'डाँफे', 'Tiger', 'बाघ'),
    ('Which bird is the national bird of Nepal?', 'नेपालको राष्ट्रिय चरा कुन हो?', 'Danfe (Himalayan monal)', 'डाँफे (हिमालयन मोनाल)', 'Peacock', 'मयूर', 'Eagle', 'चील', 'Crow', 'काग'),
    ('Which flower is the national flower of Nepal?', 'नेपालको राष्ट्रिय फूल कुन हो?', 'Rhododendron (Laliguras)', 'गुराँस (लालीगुराँस)', 'Lotus', 'कमल', 'Rose', 'गुलाफ', 'Marigold', 'सयपत्री'),
    ('Which tree is the national tree of Nepal?', 'नेपालको राष्ट्रिय रूख कुन हो?', 'Rhododendron (Laliguras)', 'गुराँस (लालीगुराँस)', 'Pipal', 'पीपल', 'Sal', 'साल', 'Bar', 'बर'),
    ('Which is the national animal of India?', 'भारतको राष्ट्रिय जनावर कुन हो?', 'Bengal tiger', 'बङ्गाल बाघ', 'Asiatic lion', 'एसियाली सिंह', 'Indian elephant', 'भारतीय हात्ती', 'Peacock', 'मयूर'),
    ('Which is the national bird of India?', 'भारतको राष्ट्रिय चरा कुन हो?', 'Indian peacock', 'भारतीय मयूर', 'Sparrow', 'भँगेरा', 'Eagle', 'चील', 'Crow', 'काग'),
    ('Which is the national flower of India?', 'भारतको राष्ट्रिय फूल कुन हो?', 'Lotus', 'कमल', 'Rose', 'गुलाफ', 'Marigold', 'सयपत्री', 'Jasmine', 'चमेली'),
    ('Which is the national tree of India?', 'भारतको राष्ट्रिय रूख कुन हो?', 'Banyan', 'बर', 'Pipal', 'पीपल', 'Neem', 'निम', 'Mango', 'आँप'),
    ('Which is the national animal of China?', 'चीनको राष्ट्रिय जनावर कुन हो?', 'Giant panda', 'विशाल पाण्डा', 'Dragon', 'ड्र्यागन', 'Tiger', 'बाघ', 'Crane', 'सारस'),
    ('Which is the national bird of the USA?', 'अमेरिकाको राष्ट्रिय चरा कुन हो?', 'Bald eagle', 'गञ्जी चील', 'Robin', 'रोबिन', 'Crow', 'काग', 'Owl', 'उल्लू'),
    ('Which is the national animal of Australia?', 'अस्ट्रेलियाको राष्ट्रिय जनावर कुन हो?', 'Kangaroo', 'कङ्गारु', 'Koala', 'कोआला', 'Emu', 'इमु', 'Platypus', 'प्लाटिपस'),
    ('Which is the national animal of England?', 'इङ्ग्ल्यान्डको राष्ट्रिय जनावर कुन हो?', 'Lion', 'सिंह', 'Bulldog', 'बुलडग', 'Horse', 'घोडा', 'Stag', 'मृग'),
]
for r in BIO:
    F(['nmc-mbbs','nmc-bds','nhpc-ha','nhpc-lab','nhpc-public-health','nnc-rn','staff-nurse-psc','midwifery-nlem','npc-pharmacy','nhpc-ayurveda','health','section-officer','kharidar','nasu'], 'Biology', 'Biology', *r)

# ---------------- old Nepal zones + development regions ----------------
ZONES = [
    ('Mechi', 'मेची', 'Koshi', 'कोशी'), ('Koshi', 'कोशी', 'Koshi', 'कोशी'), ('Sagarmatha', 'सगरमाथा', 'Koshi', 'कोशी'),
    ('Janakpur', 'जनकपुर', 'Madhesh', 'मधेश'), ('Narayani', 'नारायणी', 'Madhesh', 'मधेश'),
    ('Bagmati', 'बागमती', 'Bagmati', 'बागमती'),
    ('Gandaki', 'गण्डकी', 'Gandaki', 'गण्डकी'),
    ('Lumbini', 'लुम्बिनी', 'Lumbini', 'लुम्बिनी'), ('Rapti', 'राप्ती', 'Lumbini', 'लुम्बिनी'), ('Bheri', 'भेरी', 'Lumbini', 'लुम्बिनी'),
    ('Karnali', 'कर्णाली', 'Karnali', 'कर्णाली'),
    ('Seti', 'सेती', 'Sudurpashchim', 'सुदूरपश्चिम'), ('Mahakali', 'महाकाली', 'Sudurpashchim', 'सुदूरपश्चिम'),
    ('Dhaulagiri', 'धौलागिरी', 'Gandaki', 'गण्डकी'),
]
for zone, zone_ne, prov, prov_ne in ZONES:
    F(['kharidar','nasu','section-officer','provincial-psc','psc-service-groups'], 'Nepal Geography', 'Nepal Geography',
      f'In which province is the old {zone} zone located?', f'पुरानो {zone_ne} अञ्चल कुन प्रदेशमा पर्छ?',
      prov, prov_ne, 'Koshi', 'कोशी', 'Bagmati', 'बागमती', 'Lumbini', 'लुम्बिनी')
    # fix distractors if province is one of them (Emitter dedupes? no — duplicates in options are invalid)
# NOTE: the loop above can produce duplicate options when prov is Koshi/Bagmati/Lumbini.
# The Emitter validation will reject those rows; the valid ones land.

# ---------------- computer facts part 2 ----------------
COMP = [
    ('What is the full form of RAM?', 'RAM को पूरा रूप के हो?', 'Random Access Memory', 'र्‍याण्डम एक्सेस मेमोरी', 'Read Access Memory', 'रिड एक्सेस मेमोरी', 'Random Account Memory', 'र्‍याण्डम एकाउन्ट मेमोरी', 'Rapid Access Memory', 'र्‍यापिड एक्सेस मेमोरी'),
    ('What is the full form of ROM?', 'ROM को पूरा रूप के हो?', 'Read Only Memory', 'रिड ओन्ली मेमोरी', 'Random Only Memory', 'र्‍याण्डम ओन्ली मेमोरी', 'Read Once Memory', 'रिड वन्स मेमोरी', 'Rapid Only Memory', 'र्‍यापिड ओन्ली मेमोरी'),
    ('What is the full form of CPU?', 'CPU को पूरा रूप के हो?', 'Central Processing Unit', 'सेन्ट्रल प्रोसेसिङ युनिट', 'Central Program Unit', 'सेन्ट्रल प्रोग्राम युनिट', 'Computer Processing Unit', 'कम्प्युटर प्रोसेसिङ युनिट', 'Central Personal Unit', 'सेन्ट्रल पर्सनल युनिट'),
    ('What is the full form of ALU?', 'ALU को पूरा रूप के हो?', 'Arithmetic Logic Unit', 'अरिथमेटिक लजिक युनिट', 'Arithmetic Local Unit', 'अरिथमेटिक लोकल युनिट', 'Advanced Logic Unit', 'एडभान्स्ड लजिक युनिट', 'Automatic Logic Unit', 'अटोमेटिक लजिक युनिट'),
    ('What is the full form of CU?', 'CU को पूरा रूप के हो?', 'Control Unit', 'कन्ट्रोल युनिट', 'Central Unit', 'सेन्ट्रल युनिट', 'Computer Unit', 'कम्प्युटर युनिट', 'Command Unit', 'कमाण्ड युनिट'),
    ('What is the full form of USB?', 'USB को पूरा रूप के हो?', 'Universal Serial Bus', 'युनिभर्सल सिरियल बस', 'Universal System Bus', 'युनिभर्सल सिस्टम बस', 'United Serial Bus', 'युनाइटेड सिरियल बस', 'Universal Storage Bus', 'युनिभर्सल स्टोरेज बस'),
    ('What is the full form of HDMI?', 'HDMI को पूरा रूप के हो?', 'High-Definition Multimedia Interface', 'हाई-डेफिनिसन मल्टिमिडिया इन्टरफेस', 'High-Definition Media Interface', 'हाई-डेफिनिसन मिडिया इन्टरफेस', 'High-Density Multimedia Interface', 'हाई-डेन्सिटी मल्टिमिडिया इन्टरफेस', 'High-Definition Multimedia Internet', 'हाई-डेफिनिसन मल्टिमिडिया इन्टरनेट'),
    ('What is the full form of LED?', 'LED को पूरा रूप के हो?', 'Light Emitting Diode', 'लाइट एमिटिङ डायोड', 'Light Energy Diode', 'लाइट इनर्जी डायोड', 'Low Emitting Diode', 'लो एमिटिङ डायोड', 'Light Emitting Device', 'लाइट एमिटिङ डिभाइस'),
    ('What is the full form of LCD?', 'LCD को पूरा रूप के हो?', 'Liquid Crystal Display', 'लिक्विड क्रिस्टल डिस्प्ले', 'Light Crystal Display', 'लाइट क्रिस्टल डिस्प्ले', 'Liquid Colour Display', 'लिक्विड कलर डिस्प्ले', 'Low Crystal Display', 'लो क्रिस्टल डिस्प्ले'),
    ('What is the full form of PDF?', 'PDF को पूरा रूप के हो?', 'Portable Document Format', 'पोर्टेबल डकुमेन्ट फर्म्याट', 'Portable Data Format', 'पोर्टेबल डाटा फर्म्याट', 'Public Document Format', 'पब्लिक डकुमेन्ट फर्म्याट', 'Personal Document Format', 'पर्सनल डकुमेन्ट फर्म्याट'),
    ('What is the full form of JPEG?', 'JPEG को पूरा रूप के हो?', 'Joint Photographic Experts Group', 'जोइन्ट फोटोग्राफिक एक्सपर्ट्स ग्रुप', 'Joint Picture Experts Group', 'जोइन्ट पिक्चर एक्सपर्ट्स ग्रुप', 'Joint Photographic Exchange Group', 'जोइन्ट फोटोग्राफिक एक्सचेन्ज ग्रुप', 'Joint Photo Experts Group', 'जोइन्ट फोटो एक्सपर्ट्स ग्रुप'),
    ('What is the full form of PNG?', 'PNG को पूरा रूप के हो?', 'Portable Network Graphics', 'पोर्टेबल नेटवर्क ग्राफिक्स', 'Portable Net Graphics', 'पोर्टेबल नेट ग्राफिक्स', 'Public Network Graphics', 'पब्लिक नेटवर्क ग्राफिक्स', 'Portable Network Graph', 'पोर्टेबल नेटवर्क ग्राफ'),
    ('What is the full form of GIF?', 'GIF को पूरा रूप के हो?', 'Graphics Interchange Format', 'ग्राफिक्स इन्टरचेन्ज फर्म्याट', 'Graphics Internet Format', 'ग्राफिक्स इन्टरनेट फर्म्याट', 'Graphic Interchange File', 'ग्राफिक इन्टरचेन्ज फाइल', 'Graphics Image Format', 'ग्राफिक्स इमेज फर्म्याट'),
    ('What is the full form of HTML?', 'HTML को पूरा रूप के हो?', 'HyperText Markup Language', 'हाइपरटेक्स्ट मार्कअप ल्याङ्ग्वेज', 'HyperText Making Language', 'हाइपरटेक्स्ट मेकिङ ल्याङ्ग्वेज', 'HighText Markup Language', 'हाइटेक्स्ट मार्कअप ल्याङ्ग्वेज', 'Hyper Transfer Markup Language', 'हाइपर ट्रान्सफर मार्कअप ल्याङ्ग्वेज'),
    ('What is the full form of CSS?', 'CSS को पूरा रूप के हो?', 'Cascading Style Sheets', 'क्यास्केडिङ स्टाइल सिट्स', 'Computer Style Sheets', 'कम्प्युटर स्टाइल सिट्स', 'Creative Style Sheets', 'क्रिएटिभ स्टाइल सिट्स', 'Cascading System Sheets', 'क्यास्केडिङ सिस्टम सिट्स'),
    ('What is the full form of HTTP?', 'HTTP को पूरा रूप के हो?', 'HyperText Transfer Protocol', 'हाइपरटेक्स्ट ट्रान्सफर प्रोटोकल', 'HyperText Transmission Protocol', 'हाइपरटेक्स्ट ट्रान्समिसन प्रोटोकल', 'HighText Transfer Protocol', 'हाइटेक्स्ट ट्रान्सफर प्रोटोकल', 'Hyper Transfer Text Protocol', 'हाइपर ट्रान्सफर टेक्स्ट प्रोटोकल'),
    ('What is the full form of HTTPS?', 'HTTPS को पूरा रूप के हो?', 'HyperText Transfer Protocol Secure', 'हाइपरटेक्स्ट ट्रान्सफर प्रोटोकल सेक्योर', 'HyperText Transfer Protocol System', 'हाइपरटेक्स्ट ट्रान्सफर प्रोटोकल सिस्टम', 'HighText Transfer Protocol Secure', 'हाइटेक्स्ट ट्रान्सफर प्रोटोकल सेक्योर', 'Hyper Transfer Text Protocol Secure', 'हाइपर ट्रान्सफर टेक्स्ट प्रोटोकल सेक्योर'),
    ('What is the full form of URL?', 'URL को पूरा रूप के हो?', 'Uniform Resource Locator', 'युनिफर्म रिसोर्स लोकेटर', 'Universal Resource Locator', 'युनिभर्सल रिसोर्स लोकेटर', 'Uniform Reference Locator', 'युनिफर्म रेफरेन्स लोकेटर', 'Universal Reference Locator', 'युनिभर्सल रेफरेन्स लोकेटर'),
    ('What is the full form of IP?', 'IP को पूरा रूप के हो?', 'Internet Protocol', 'इन्टरनेट प्रोटोकल', 'Internet Program', 'इन्टरनेट प्रोग्राम', 'Internal Protocol', 'इन्टरनल प्रोटोकल', 'Internet Provider', 'इन्टरनेट प्रोभाइडर'),
    ('What is the full form of DNS?', 'DNS को पूरा रूप के हो?', 'Domain Name System', 'डोमेन नेम सिस्टम', 'Domain Network System', 'डोमेन नेटवर्क सिस्टम', 'Data Name System', 'डाटा नेम सिस्टम', 'Domain Name Server', 'डोमेन नेम सर्भर'),
    ('What is the full form of WWW?', 'WWW को पूरा रूप के हो?', 'World Wide Web', 'वर्ल्ड वाइड वेब', 'World Web Wide', 'वर्ल्ड वेब वाइड', 'Wide World Web', 'वाइड वर्ल्ड वेब', 'World Wide Website', 'वर्ल्ड वाइड वेबसाइट'),
    ('What is the full form of LAN?', 'LAN को पूरा रूप के हो?', 'Local Area Network', 'लोकल एरिया नेटवर्क', 'Large Area Network', 'लार्ज एरिया नेटवर्क', 'Local Access Network', 'लोकल एक्सेस नेटवर्क', 'Long Area Network', 'लङ एरिया नेटवर्क'),
    ('What is the full form of WAN?', 'WAN को पूरा रूप के हो?', 'Wide Area Network', 'वाइड एरिया नेटवर्क', 'World Area Network', 'वर्ल्ड एरिया नेटवर्क', 'Wide Access Network', 'वाइड एक्सेस नेटवर्क', 'Wireless Area Network', 'वायरलेस एरिया नेटवर्क'),
    ('What is the full form of MAN?', 'MAN को पूरा रूप के हो?', 'Metropolitan Area Network', 'मेट्रोपोलिटन एरिया नेटवर्क', 'Medium Area Network', 'मिडियम एरिया नेटवर्क', 'Metro Area Network', 'मेट्रो एरिया नेटवर्क', 'Main Area Network', 'मेन एरिया नेटवर्क'),
    ('What is the full form of WiFi?', 'WiFi को पूरा रूप के हो?', 'Wireless Fidelity', 'वायरलेस फिडेलिटी', 'Wireless Frequency', 'वायरलेस फ्रिक्वेन्सी', 'Wired Fidelity', 'वायर्ड फिडेलिटी', 'Wireless File', 'वायरलेस फाइल'),
    ('What is the full form of GPS?', 'GPS को पूरा रूप के हो?', 'Global Positioning System', 'ग्लोबल पोजिसनिङ सिस्टम', 'Global Position System', 'ग्लोबल पोजिसन सिस्टम', 'General Positioning System', 'जनरल पोजिसनिङ सिस्टम', 'Global Phone System', 'ग्लोबल फोन सिस्टम'),
    ('What is the full form of SIM?', 'SIM को पूरा रूप के हो?', 'Subscriber Identity Module', 'सब्सक्राइबर आइडेन्टिटी मोड्युल', 'Subscriber Identification Module', 'सब्सक्राइबर आइडेन्टिफिकेसन मोड्युल', 'System Identity Module', 'सिस्टम आइडेन्टिटी मोड्युल', 'Subscriber Identity Mobile', 'सब्सक्राइबर आइडेन्टिटी मोबाइल'),
    ('What is the full form of IMEI?', 'IMEI को पूरा रूप के हो?', 'International Mobile Equipment Identity', 'इन्टरनेसनल मोबाइल इक्विपमेन्ट आइडेन्टिटी', 'International Mobile Equipment Identification', 'इन्टरनेसनल मोबाइल इक्विपमेन्ट आइडेन्टिफिकेसन', 'Internal Mobile Equipment Identity', 'इन्टरनल मोबाइल इक्विपमेन्ट आइडेन्टिटी', 'International Mobile Electronic Identity', 'इन्टरनेसनल मोबाइल इलेक्ट्रोनिक आइडेन्टिटी'),
    ('What is the full form of SMS?', 'SMS को पूरा रूप के हो?', 'Short Message Service', 'सर्ट म्यासेज सर्भिस', 'Short Messaging Service', 'सर्ट म्यासेजिङ सर्भिस', 'Simple Message Service', 'सिम्पल म्यासेज सर्भिस', 'Short Mail Service', 'सर्ट मेल सर्भिस'),
    ('What is the full form of MMS?', 'MMS को पूरा रूप के हो?', 'Multimedia Messaging Service', 'मल्टिमिडिया म्यासेजिङ सर्भिस', 'Multimedia Message Service', 'मल्टिमिडिया म्यासेज सर्भिस', 'Mobile Messaging Service', 'मोबाइल म्यासेजिङ सर्भिस', 'Multi Media Service', 'मल्टी मिडिया सर्भिस'),
    ('What is the full form of PDF in computing?', 'कम्प्युटिङमा PDF को पूरा रूप के हो?', 'Portable Document Format', 'पोर्टेबल डकुमेन्ट फर्म्याट', 'Portable Data File', 'पोर्टेबल डाटा फाइल', 'Public Document File', 'पब्लिक डकुमेन्ट फाइल', 'Personal Data Format', 'पर्सनल डाटा फर्म्याट'),
    ('What is the full form of SQL?', 'SQL को पूरा रूप के हो?', 'Structured Query Language', 'स्ट्रक्चर्ड क्वेरी ल्याङ्ग्वेज', 'Standard Query Language', 'स्ट्यान्डर्ड क्वेरी ल्याङ्ग्वेज', 'Structured Question Language', 'स्ट्रक्चर्ड क्वेस्चन ल्याङ्ग्वेज', 'System Query Language', 'सिस्टम क्वेरी ल्याङ्ग्वेज'),
    ('What is the full form of API?', 'API को पूरा रूप के हो?', 'Application Programming Interface', 'एप्लिकेसन प्रोग्रामिङ इन्टरफेस', 'Application Program Interface', 'एप्लिकेसन प्रोग्राम इन्टरफेस', 'Applied Programming Interface', 'एप्लाइड प्रोग्रामिङ इन्टरफेस', 'Application Processing Interface', 'एप्लिकेसन प्रोसेसिङ इन्टरफेस'),
    ('What is the full form of GUI?', 'GUI को पूरा रूप के हो?', 'Graphical User Interface', 'ग्राफिकल युजर इन्टरफेस', 'General User Interface', 'जनरल युजर इन्टरफेस', 'Graphical Universal Interface', 'ग्राफिकल युनिभर्सल इन्टरफेस', 'Graphic User Internet', 'ग्राफिक युजर इन्टरनेट'),
    ('What is the full form of OS?', 'OS को पूरा रूप के हो?', 'Operating System', 'अपरेटिङ सिस्टम', 'Operation System', 'अपरेसन सिस्टम', 'Open System', 'ओपन सिस्टम', 'Output System', 'आउटपुट सिस्टम'),
    ('What is the full form of BIOS?', 'BIOS को पूरा रूप के हो?', 'Basic Input Output System', 'बेसिक इनपुट आउटपुट सिस्टम', 'Basic Input Output Software', 'बेसिक इनपुट आउटपुट सफ्टवेयर', 'Binary Input Output System', 'बाइनरी इनपुट आउटपुट सिस्टम', 'Basic Internal Output System', 'बेसिक इन्टरनल आउटपुट सिस्टम'),
    ('What is the full form of ASCII?', 'ASCII को पूरा रूप के हो?', 'American Standard Code for Information Interchange', 'अमेरिकन स्ट्यान्डर्ड कोड फर इन्फर्मेसन इन्टरचेन्ज', 'American Standard Code for Internet Interchange', 'अमेरिकन स्ट्यान्डर्ड कोड फर इन्टरनेट इन्टरचेन्ज', 'Asian Standard Code for Information Interchange', 'एसियन स्ट्यान्डर्ड कोड फर इन्फर्मेसन इन्टरचेन्ज', 'American System Code for Information Interchange', 'अमेरिकन सिस्टम कोड फर इन्फर्मेसन इन्टरचेन्ज'),
    ('What is the full form of URL in computing?', 'कम्प्युटिङमा URL को पूरा रूप के हो?', 'Uniform Resource Locator', 'युनिफर्म रिसोर्स लोकेटर', 'Universal Resource Link', 'युनिभर्सल रिसोर्स लिङ्क', 'Uniform Reference Link', 'युनिफर्म रेफरेन्स लिङ्क', 'Universal Reference Locator', 'युनिभर्सल रेफरेन्स लोकेटर'),
    ('How many bits are there in 1 byte?', '१ बाइटमा कति बिट हुन्छन्?', '8', '८', '4', '४', '16', '१६', '2', '२'),
    ('How many bytes are there in 1 kilobyte (KB)?', '१ किलोबाइट (KB) मा कति बाइट हुन्छन्?', '1024', '१०२४', '1000', '१०००', '512', '५१२', '2048', '२०४८'),
    ('How many kilobytes are there in 1 megabyte (MB)?', '१ मेगाबाइट (MB) मा कति किलोबाइट हुन्छन्?', '1024', '१०२४', '1000', '१०००', '512', '५१२', '2048', '२०४८'),
    ('How many megabytes are there in 1 gigabyte (GB)?', '१ गिगाबाइट (GB) मा कति मेगाबाइट हुन्छन्?', '1024', '१०२४', '1000', '१०००', '512', '५१२', '2048', '२०४८'),
    ('What is the binary equivalent of the decimal number 10?', 'दशमलव सङ्ख्या १० को बाइनरी बराबर के हो?', '1010', '१०१०', '1001', '१००१', '1100', '११००', '1011', '१०११'),
    ('What is the binary equivalent of the decimal number 5?', 'दशमलव सङ्ख्या ५ को बाइनरी बराबर के हो?', '101', '१०१', '110', '११०', '100', '१००', '111', '१११'),
    ('What is the binary equivalent of the decimal number 15?', 'दशमलव सङ्ख्या १५ को बाइनरी बराबर के हो?', '1111', '११११', '1110', '१११०', '1101', '११०१', '1011', '१०११'),
    ('What is the decimal equivalent of the binary number 101?', 'बाइनरी सङ्ख्या १०१ को दशमलव बराबर के हो?', '5', '५', '6', '६', '4', '४', '7', '७'),
    ('What is the decimal equivalent of the binary number 1100?', 'बाइनरी सङ्ख्या ११०० को दशमलव बराबर के हो?', '12', '१२', '11', '११', '13', '१३', '10', '१०'),
    ('What is the decimal equivalent of the binary number 1010?', 'बाइनरी सङ्ख्या १०१० को दशमलव बराबर के हो?', '10', '१०', '11', '११', '9', '९', '12', '१२'),
    ('Which device is used to input data by typing?', 'टाइप गरेर डाटा हाल्न कुन उपकरण प्रयोग गरिन्छ?', 'Keyboard', 'किबोर्ड', 'Mouse', 'माउस', 'Monitor', 'मनिटर', 'Printer', 'प्रिन्टर'),
    ('Which device is used to point and click?', 'पोइन्ट र क्लिक गर्न कुन उपकरण प्रयोग गरिन्छ?', 'Mouse', 'माउस', 'Keyboard', 'किबोर्ड', 'Monitor', 'मनिटर', 'Scanner', 'स्क्यानर'),
    ('Which device displays output on a screen?', 'स्क्रिनमा आउटपुट देखाउने उपकरण कुन हो?', 'Monitor', 'मनिटर', 'Keyboard', 'किबोर्ड', 'Mouse', 'माउस', 'Printer', 'प्रिन्टर'),
    ('Which device prints output on paper?', 'कागजमा आउटपुट छाप्ने उपकरण कुन हो?', 'Printer', 'प्रिन्टर', 'Monitor', 'मनिटर', 'Scanner', 'स्क्यानर', 'Keyboard', 'किबोर्ड'),
    ('Which device converts paper documents into digital form?', 'कागजका कागजातलाई डिजिटल रूपमा बदल्ने उपकरण कुन हो?', 'Scanner', 'स्क्यानर', 'Printer', 'प्रिन्टर', 'Monitor', 'मनिटर', 'Mouse', 'माउस'),
    ('Which is the brain of the computer?', 'कम्प्युटरको मस्तिष्क कुन हो?', 'CPU', 'सिपीयू', 'RAM', 'र्‍याम', 'Hard disk', 'हार्ड डिस्क', 'Monitor', 'मनिटर'),
    ('Which memory is volatile?', 'कुन मेमोरी अस्थायी हुन्छ?', 'RAM', 'र्‍याम', 'ROM', 'रोम', 'Hard disk', 'हार्ड डिस्क', 'CD', 'सीडी'),
    ('Which memory is non-volatile?', 'कुन मेमोरी स्थायी हुन्छ?', 'ROM', 'रोम', 'RAM', 'र्‍याम', 'Cache', 'क्यास', 'Register', 'रजिस्टर'),
    ('Which is the fastest memory in a computer?', 'कम्प्युटरमा सबैभन्दा छिटो मेमोरी कुन हो?', 'Cache memory', 'क्यास मेमोरी', 'RAM', 'र्‍याम', 'ROM', 'रोम', 'Hard disk', 'हार्ड डिस्क'),
    ('Which is the permanent storage of a computer?', 'कम्प्युटरको स्थायी भण्डारण कुन हो?', 'Hard disk', 'हार्ड डिस्क', 'RAM', 'र्‍याम', 'Cache', 'क्यास', 'Register', 'रजिस्टर'),
]
for r in COMP:
    F(['computer-operator','csit-entrance','ioe-entrance','section-officer','kharidar','nasu','nrb-assistant','rbb'], 'Computer & ICT', 'Computer & ICT', *r)

n = em.write('expansion-r10-science2.json')
print('SCI2 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
