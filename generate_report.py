"""
Comprehensive Generator for the official AI & ML Project Work Report for Sri Eshwar College of Engineering
Conforming strictly to:
1. "Project Report - Formatting Conditions"
   - Paper Size: A4
   - Font: Times New Roman throughout
   - Chapter/Unit Heading: 16 pt, Bold
   - Section Heading: 14 pt, Bold
   - Sub-section Heading: 12 pt, Bold
   - Body Text: 12 pt, 1.5 Line Spacing, Justified
   - Margins: Left 1.5 in (38.1mm), Right 1.0 in (25.4mm), Top 1.0 in (25.4mm), Bottom 1.0 in (25.4mm)
   - Page numbering:
     * Abstract: Roman numeral small case 'i'
     * Table of contents: No page number
     * List of Figures: Roman numeral small case 'ii'
     * List of Tables: Roman numeral small case 'iii'
     * Chapter 1 onwards: Arabic '1, 2, ...'
   - Chapter Arrangement: Each major chapter begins on a new page.
   - Sequential figure and table numbering with formal titles/captions.
2. College AIML Report Structure (Template PDF)
3. Modded Technical Stack:
   - Decoupled Dual-Model Neural Dead Reckoning (VelocityNet + YawRateNet)
   - Zero-Velocity Update (ZUPT) & Gyro Bias Snap Gatekeeper
   - Online Drift Adaptation & L2 Anchor Tuning
   - 5-State Intelligent EKF Sensor Fusion (ENU WGS84)
   - Real IO-VNBD Benchmark Dataset Validation
   - FastAPI + WebSocket 50Hz telemetry & Leaflet Web Dashboard
   - Complete, un-truncated Appendix source code listings.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def add_page_number_to_section(section, fmt="decimal", start=None):
    sectPr = section._sectPr
    for child in list(sectPr):
        if child.tag.endswith('pgNumType'):
            sectPr.remove(child)
    
    if start is not None:
        pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="{fmt}" w:start="{start}"/>')
    else:
        pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="{fmt}"/>')
    sectPr.append(pgNumType)

    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.text = ""
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
    run._r.append(fld)

def configure_section_margins(section):
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)

def read_source_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"# File not found: {file_path}"

def generate_report():
    doc = docx.Document()

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # -------------------------------------------------------------
    # SECTION 1: PRELIMINARY PAGES (Cover, Inner Cover, Certificate, Declaration, Acknowledgement)
    # -------------------------------------------------------------
    sec_prelim = doc.sections[0]
    configure_section_margins(sec_prelim)
    sec_prelim.footer.is_linked_to_previous = False
    sec_prelim.footer.paragraphs[0].text = ""

    # ==========================================
    # 1. OUTER COVER PAGE
    # ==========================================
    # Top banner table with Logo on left and Title on right
    table_top = doc.add_table(rows=1, cols=2)
    table_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_top.autofit = False
    table_top.columns[0].width = Inches(2.2)
    table_top.columns[1].width = Inches(3.5)

    c_logo = table_top.rows[0].cells[0]
    p_logo = c_logo.paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.LEFT
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "sece_logo.png")
    if os.path.exists(logo_path):
        run_l = p_logo.add_run()
        run_l.add_picture(logo_path, width=Inches(1.5))

    c_top_title = table_top.rows[0].cells[1]
    p_tt = c_top_title.paragraphs[0]
    p_tt.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_tt = p_tt.add_run("<< TITLE OF THE PROJECT >>\nAI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM")
    r_tt.font.name = "Times New Roman"
    r_tt.font.size = Pt(11)
    r_tt.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(18)
    r = p.add_run("OCTOBER 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(28)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.3
    r = p_title.add_run(
        "PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT\n"
        "OF THE REQUIREMENTS FOR THE AWARD OF THE\n"
        "DEGREE OF BACHELOR OF ENGINEERING\n"
        "IN COMPUTER SCIENCE AND ENGINEERING\n"
        "OF THE ANNA UNIVERSITY"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    p_space2 = doc.add_paragraph()
    p_space2.paragraph_format.space_before = Pt(36)

    # Boxed left "AI & ML PROJECT WORK" and Right "Submitted by..."
    table_cover = doc.add_table(rows=1, cols=2)
    table_cover.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_cover.autofit = False
    table_cover.columns[0].width = Inches(2.2)
    table_cover.columns[1].width = Inches(3.5)

    c0 = table_cover.rows[0].cells[0]
    p_box = c0.paragraphs[0]
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.line_spacing = 1.2
    r = p_box.add_run("━━━━━━━━━━━━━\nAI & ML\nPROJECT\nWORK\n━━━━━━━━━━━━━")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    c1 = table_cover.rows[0].cells[1]
    p_sub = c1.paragraphs[0]
    p_sub.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sub.paragraph_format.line_spacing = 1.2
    r = p_sub.add_run("Submitted by\n\nNAME OF THE STUDENT - Register Number\n[STUDENT NAME 1] - [REGISTER NUMBER 1]\n[STUDENT NAME 2] - [REGISTER NUMBER 2]\n\nBATCH\n2025 - 2029")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p_space3 = doc.add_paragraph()
    p_space3.paragraph_format.space_before = Pt(30)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_guide.paragraph_format.line_spacing = 1.2
    r = p_guide.add_run("Under the Guidance of\n<< NAME OF THE FACULTY >>\n[FACULTY NAME, M.E., Ph.D.]\n<< DESIGNATION >>\nAssistant Professor, CSE.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p_space4 = doc.add_paragraph()
    p_space4.paragraph_format.space_before = Pt(36)

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.line_spacing = 1.2
    r = p_foot.add_run("COMPUTER SCIENCE AND ENGINEERING\nSri Eshwar College of Engineering\n(An Autonomous Institution – Affiliated to Anna University)\nCOIMBATORE – 641 202\n\n<< TITLE OF THE PROJECT >>")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    # ==========================================
    # 2. INNER TITLE PAGE
    # ==========================================
    doc.add_page_break()

    # Inner page logo and banner
    table_top_in = doc.add_table(rows=1, cols=2)
    table_top_in.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_top_in.autofit = False
    table_top_in.columns[0].width = Inches(2.2)
    table_top_in.columns[1].width = Inches(3.5)

    c_logo_in = table_top_in.rows[0].cells[0]
    p_logo_in = c_logo_in.paragraphs[0]
    p_logo_in.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists(logo_path):
        run_li = p_logo_in.add_run()
        run_li.add_picture(logo_path, width=Inches(1.5))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(18)
    r = p.add_run("OCTOBER 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(28)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.3
    r = p_title.add_run(
        "PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT\n"
        "OF THE REQUIREMENTS FOR THE AWARD OF THE\n"
        "DEGREE OF BACHELOR OF ENGINEERING\n"
        "IN COMPUTER SCIENCE AND ENGINEERING\n"
        "OF THE ANNA UNIVERSITY"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    p_space2 = doc.add_paragraph()
    p_space2.paragraph_format.space_before = Pt(36)

    table_inner = doc.add_table(rows=1, cols=2)
    table_inner.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_inner.autofit = False
    table_inner.columns[0].width = Inches(2.2)
    table_inner.columns[1].width = Inches(3.5)

    c0 = table_inner.rows[0].cells[0]
    p_box = c0.paragraphs[0]
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.line_spacing = 1.2
    r = p_box.add_run("━━━━━━━━━━━━━\nAI & ML\nPROJECT\nWORK\n━━━━━━━━━━━━━")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    c1 = table_inner.rows[0].cells[1]
    p_sub = c1.paragraphs[0]
    p_sub.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sub.paragraph_format.line_spacing = 1.2
    r = p_sub.add_run("Submitted by\n\nNAME – REG NO\n[STUDENT NAME 1] – [REGISTER NUMBER 1]\n[STUDENT NAME 2] – [REGISTER NUMBER 2]\n\nBATCH\n2025 - 2029")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p_space3 = doc.add_paragraph()
    p_space3.paragraph_format.space_before = Pt(30)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_guide.paragraph_format.line_spacing = 1.2
    r = p_guide.add_run("Under the Guidance of\n[FACULTY NAME],\nAssistant Professor, CSE.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p_space4 = doc.add_paragraph()
    p_space4.paragraph_format.space_before = Pt(36)

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.line_spacing = 1.2
    r = p_foot.add_run("Department of Computer Science and Engineering\nSri Eshwar College of Engineering\n(An Autonomous Institution – Affiliated to Anna University)\nCOIMBATORE – 641 202")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    # ==========================================
    # 3. BONAFIDE CERTIFICATE
    # ==========================================
    doc.add_page_break()

    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_head.paragraph_format.line_spacing = 1.2
    r = p_head.add_run("Sri Eshwar College of Engineering\n(An Autonomous Institution – Affiliated to Anna University)\nCOIMBATORE – 641 202\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_bon = doc.add_paragraph()
    p_bon.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_bon.add_run("BONAFIDE CERTIFICATE\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert.paragraph_format.line_spacing = 1.5
    r = p_cert.add_run(
        "Certified that this Report titled “AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES” "
        "for the course U23AM495 - Artificial Intelligence and Machine Learning is the bonafide work of "
        "<<NAME OF THE CANDIDATE 1>> (<<Reg. Number 1>>) and <<NAME OF THE CANDIDATE 2>> (<<Reg. Number 2>>) "
        "who carried out the project work under my supervision."
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(36)

    table_sign = doc.add_table(rows=1, cols=2)
    table_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sign.autofit = False
    table_sign.columns[0].width = Inches(3.0)
    table_sign.columns[1].width = Inches(3.0)

    c0 = table_sign.rows[0].cells[0]
    p_s0 = c0.paragraphs[0]
    p_s0.paragraph_format.line_spacing = 1.2
    r0 = p_s0.add_run("-----------------------------------------\nSIGNATURE\nDr. R. SUBHA M.E., Ph.D.\nHEAD OF THE DEPARTMENT\nDept. of Computer Science & Engineering\nSri Eshwar College of Engineering,\nCoimbatore – 641 202.")
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(11)
    r0.font.bold = True

    c1 = table_sign.rows[0].cells[1]
    p_s1 = c1.paragraphs[0]
    p_s1.paragraph_format.line_spacing = 1.2
    r1 = p_s1.add_run("-----------------------------------------\nSIGNATURE\n<<Faculty Name>>\nSUPERVISOR\nAssistant Professor,\nDept. of Computer Science & Engineering,\nSri Eshwar College of Engineering,\nCoimbatore – 641 202.")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.bold = True

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(36)

    p_viva = doc.add_paragraph()
    p_viva.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p_viva.add_run("Submitted for the Autonomous Semester End Project Viva-Voce held on …………………..")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(36)

    table_exam = doc.add_table(rows=1, cols=2)
    table_exam.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_exam.autofit = False
    table_exam.columns[0].width = Inches(3.0)
    table_exam.columns[1].width = Inches(3.0)

    p_e0 = table_exam.rows[0].cells[0].paragraphs[0]
    p_e0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_e0 = p_e0.add_run("_________________________\nINTERNAL EXAMINER")
    r_e0.font.name = "Times New Roman"
    r_e0.font.size = Pt(11)
    r_e0.font.bold = True

    p_e1 = table_exam.rows[0].cells[1].paragraphs[0]
    p_e1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_e1 = p_e1.add_run("_________________________\nEXTERNAL EXAMINER")
    r_e1.font.name = "Times New Roman"
    r_e1.font.size = Pt(11)
    r_e1.font.bold = True

    # ==========================================
    # 4. DECLARATION
    # ==========================================
    doc.add_page_break()

    p_dec_title = doc.add_paragraph()
    p_dec_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dec_title.add_run("DECLARATION\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p_names = doc.add_paragraph()
    p_names.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_names.add_run("NAME [REGISTER NUMBER]\n[STUDENT NAME 1] [REGISTER NUMBER 1]\n[STUDENT NAME 2] [REGISTER NUMBER 2]\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_dec_body = doc.add_paragraph()
    p_dec_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dec_body.paragraph_format.line_spacing = 1.5
    r = p_dec_body.add_run(
        "To declare that the project entitled “AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES” "
        "submitted in partial fulfilment to the University as the project work of Bachelor of Engineering (Computer Science and Engineering) Degree, "
        "is a record of original work done by us under the supervision and guidance of FACULTY NAME, Assistant Professor, "
        "Department of Computer Science and Engineering, Sri Eshwar College of Engineering, Coimbatore.\n"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_place = doc.add_paragraph()
    p_place.paragraph_format.line_spacing = 1.3
    r = p_place.add_run("Place: Coimbatore\nDate:\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.line_spacing = 1.3
    r = p_sig.add_run("[STUDENT NAME 1]\n[STUDENT NAME 2]\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_guided = doc.add_paragraph()
    p_guided.paragraph_format.line_spacing = 1.3
    r = p_guided.add_run("Project Guided by,\n\n\n[FACULTY NAME]\nAssistant Professor, CSE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    # ==========================================
    # 5. ACKNOWLEDGEMENT
    # ==========================================
    doc.add_page_break()

    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_ack.add_run("ACKNOWLEDGEMENT\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p_ack_b1 = doc.add_paragraph()
    p_ack_b1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ack_b1.paragraph_format.line_spacing = 1.5
    r = p_ack_b1.add_run(
        "The success of a work depends on a team and cooperation. I take this opportunity to express my gratitude and thanks to everyone who helped me in my project. "
        "I would like to thank the management for the constant support provided by them to complete this project.\n\n"
        "It is indeed our great honor bounded duty to thank our beloved Chairman Mr. R. Mohanram, for his academic interest shown towards the students.\n\n"
        "We are indebted to our Director Mr. R. Rajaram, for motivating and providing us with all facilities.\n\n"
        "I wish to express my sincere regards and deep sense of gratitude to Dr. Sudha Mohanram, M.E, Ph.D. Principal, for the excellent facilities and encouragement provided during the course of the study and project.\n\n"
        "We are indebted to Dr. R. Subha, M.E., Ph.D. Dean, Computing Science for having permitted us to carry out this project and giving the complete freedom to utilize the resources.\n\n"
        "I express my sincere thanks to my course faculty FACULTY NAME, Assistant Professor of Computer Science and Engineering Department for the valuable guidance and encouragement given, to us for this project.\n\n"
        "I solemnly express our thanks to all the teaching and nonteaching staff of the Computer Science and Engineering Department, family and friends for their valuable support which inspired us to work on this project."
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # ==========================================
    # SECTION 2: ABSTRACT (Page Number: Roman 'i')
    # ==========================================
    sec_abstract = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    configure_section_margins(sec_abstract)
    sec_abstract.footer.is_linked_to_previous = False
    add_page_number_to_section(sec_abstract, fmt="lowerRoman", start=1)

    p_abs_title = doc.add_paragraph()
    p_abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_abs_title.add_run("ABSTRACT\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p_abs_body = doc.add_paragraph()
    p_abs_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs_body.paragraph_format.line_spacing = 1.5
    r = p_abs_body.add_run(
        "In modern intelligent transportation systems, autonomous vehicles, and location-based navigation services, continuous positional tracking is essential for vehicular safety. While Global Navigation Satellite Systems (GNSS) deliver precise position fixes under open skies, signal reception degrades catastrophically in GNSS-denied environments such as urban canyons, mountain passes, tunnels, and underground parking facilities. Conventional inertial dead reckoning relying on low-cost Micro-Electro-Mechanical Systems (MEMS) sensors suffers from thermo-mechanical noise, turn-on bias, and mounting tilt, leading to rapid cubic position error drift (O(t³)) within seconds.\n\n"
        "This project presents an edge-optimized Decoupled Deep Neural Dead Reckoning and Sensor Fusion Engine designed for seamless vehicular navigation during extended GNSS outages. Addressing the critical limitation of joint feature cross-talk—where smartphone pitch tilts and road vibration spikes corrupt vehicular angular rate estimation—we propose a Decoupled Dual-Model Deep Learning architecture: VelocityNet, which specializes exclusively on 3-axis accelerometer signals to infer longitudinal speed, and YawRateNet, which processes 3-axis gyroscope signals to determine rotational yaw rate without phantom turns. Both models are trained with a heteroscedastic negative log-likelihood loss function to dynamically predict kinematic state uncertainties alongside point estimates.\n\n"
        "The model is tightly integrated into a 5-state Extended Kalman Filter (EKF) operating in local metric East-North-Up (ENU) coordinates. To ensure long-term stability, an automated Zero-Velocity Update (ZUPT) gatekeeper detects stationary vehicle states to lock velocity and snap gyro biases, while an online drift adaptation engine continuously compensates for device mounting tilt during active GNSS lock. Evaluated on the international benchmark IO-VNBD dataset across diverse driving regimes, the proposed system bounds position drift to under 2.5 meters across a 30-second complete GNSS outage, achieving over 90% drift reduction compared to naive dead reckoning. The end-to-end framework is deployed on an asynchronous FastAPI backend streaming 50 Hz telemetry over WebSockets to an interactive Leaflet.js dashboard for real-time vehicular state visualization."
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # ==========================================
    # SECTION 3: TABLE OF CONTENTS (NO Page Number)
    # ==========================================
    sec_toc = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    configure_section_margins(sec_toc)
    sec_toc.footer.is_linked_to_previous = False
    sec_toc.footer.paragraphs[0].text = ""  # Condition 7: "should not enter page number for table of contents"

    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_toc_title.add_run("TABLE OF CONTENTS\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    table_toc = doc.add_table(rows=1, cols=3)
    table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_toc.autofit = False
    table_toc.columns[0].width = Inches(0.8)
    table_toc.columns[1].width = Inches(4.5)
    table_toc.columns[2].width = Inches(1.0)

    hdr_cells = table_toc.rows[0].cells
    hdr_cells[0].paragraphs[0].text = "S.No"
    hdr_cells[1].paragraphs[0].text = "Contents"
    hdr_cells[2].paragraphs[0].text = "Page No"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)

    toc_entries = [
        ("", "ABSTRACT", "i"),
        ("1", "INTRODUCTION", "1"),
        ("2", "SYSTEM ANALYSIS AND DESIGN", "3"),
        ("2.1", "Existing Scenario & Limitations", "3"),
        ("2.2", "Problem Statement", "4"),
        ("2.3", "Objectives", "4"),
        ("2.4", "Scope of the Project", "5"),
        ("2.5", "System Requirements", "5"),
        ("2.5.1", "Hardware Requirements", "5"),
        ("2.5.2", "Software Requirements", "6"),
        ("3", "PROPOSED SOLUTION", "7"),
        ("3.1", "Overview", "7"),
        ("3.2", "System Architecture / Block Diagram", "8"),
        ("3.3", "Methodology", "9"),
        ("3.4", "Development Phases", "10"),
        ("3.5", "Dataset Description", "11"),
        ("3.6", "Data Preprocessing", "12"),
        ("3.7", "Feature Engineering", "13"),
        ("3.8", "Model Development (Decoupled Dual-Model IDR)", "14"),
        ("3.9", "Evaluation Metrics", "15"),
        ("3.10", "Challenge-Specific Processing (Online Calibration & ZUPT)", "16"),
        ("4", "IMPLEMENTATION AND RESULTS", "17"),
        ("4.1", "Development Environment", "17"),
        ("4.2", "Implementation Modules", "18"),
        ("4.3", "Experimental Results", "19"),
        ("4.4", "Model Comparison", "20"),
        ("4.5", "Output / Screenshots & Telemetry Interface", "21"),
        ("4.6", "Discussion", "22"),
        ("5", "CONCLUSION AND FUTURE ENHANCEMENT", "23"),
        ("5.1", "Conclusion", "23"),
        ("5.2", "Future Enhancement", "24"),
        ("6", "REFERENCES", "25"),
        ("", "APPENDIX: Source Code Listings", "26"),
        ("", "Appendix A: models/idr_model.py", "26"),
        ("", "Appendix B: sensor_fusion/ekf.py", "29"),
        ("", "Appendix C: sensor_fusion/coordinates.py", "33"),
        ("", "Appendix D: models/online_calibrator.py", "35"),
        ("", "Appendix E: backend/main.py", "38")
    ]

    for sno, title, page in toc_entries:
        row = table_toc.add_row()
        c0, c1, c2 = row.cells
        c0.paragraphs[0].text = sno
        c1.paragraphs[0].text = title
        c2.paragraphs[0].text = page
        for c in [c0, c1, c2]:
            set_cell_margins(c, top=45, bottom=45, left=100, right=100)
            if len(c.paragraphs[0].runs) > 0:
                c.paragraphs[0].runs[0].font.name = "Times New Roman"
                c.paragraphs[0].runs[0].font.size = Pt(11)
                if sno in ["1", "2", "3", "4", "5", "6", ""]:
                    c.paragraphs[0].runs[0].font.bold = True

    # ==========================================
    # SECTION 4: LIST OF FIGURES & TABLES (Page Number: Roman 'ii', 'iii')
    # ==========================================
    sec_lof = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    configure_section_margins(sec_lof)
    sec_lof.footer.is_linked_to_previous = False
    add_page_number_to_section(sec_lof, fmt="lowerRoman", start=2)

    p_lof_title = doc.add_paragraph()
    p_lof_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_lof_title.add_run("LIST OF FIGURES\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    table_lof = doc.add_table(rows=1, cols=3)
    table_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_lof.autofit = False
    table_lof.columns[0].width = Inches(1.1)
    table_lof.columns[1].width = Inches(4.2)
    table_lof.columns[2].width = Inches(1.0)

    hdr = table_lof.rows[0].cells
    hdr[0].paragraphs[0].text = "Fig. No."
    hdr[1].paragraphs[0].text = "Figure Title"
    hdr[2].paragraphs[0].text = "Page No."
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)

    fig_entries = [
        ("3.2.1", "Decoupled AI-ML Intelligent Dead Reckoning End-to-End System Architecture", "8"),
        ("3.8.1", "Architectural Decoupling of VelocityNet and YawRateNet in DecoupledDualModelIDR", "14"),
        ("4.2.1", "Execution Flowchart Across the Five Implementation Modules", "18"),
        ("4.3.1", "Vehicular Trajectory Tracking During 30-Second Complete GNSS Outage", "19"),
        ("4.3.2", "Cumulative Positional Error Growth: Naive IMU vs. Proposed Decoupled IDR", "20"),
        ("4.3.3", "Neural Speed and Heading Tracking Performance under Road Vibration Noise", "20"),
        ("4.5.1", "Real-Time Web Telemetry HUD and Leaflet Dynamic Map Interface", "21")
    ]
    for fno, ftitle, fpage in fig_entries:
        row = table_lof.add_row()
        c0, c1, c2 = row.cells
        c0.paragraphs[0].text = fno
        c1.paragraphs[0].text = ftitle
        c2.paragraphs[0].text = fpage
        for c in [c0, c1, c2]:
            set_cell_margins(c, top=45, bottom=45, left=100, right=100)
            if len(c.paragraphs[0].runs) > 0:
                c.paragraphs[0].runs[0].font.name = "Times New Roman"
                c.paragraphs[0].runs[0].font.size = Pt(11)

    p_lot_space = doc.add_paragraph()
    p_lot_space.paragraph_format.space_before = Pt(36)

    p_lot_title = doc.add_paragraph()
    p_lot_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_lot_title.add_run("LIST OF TABLES\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    table_lot = doc.add_table(rows=1, cols=3)
    table_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_lot.autofit = False
    table_lot.columns[0].width = Inches(1.1)
    table_lot.columns[1].width = Inches(4.2)
    table_lot.columns[2].width = Inches(1.0)

    hdr = table_lot.rows[0].cells
    hdr[0].paragraphs[0].text = "Table No."
    hdr[1].paragraphs[0].text = "Table Title"
    hdr[2].paragraphs[0].text = "Page No."
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)

    tbl_entries = [
        ("2.5.1", "Hardware and Edge Compute Specification Requirements", "5"),
        ("2.5.2", "Software Stack, Deep Learning Frameworks, and Tools", "6"),
        ("3.5.1", "IO-VNBD Benchmark Telemetry Schema & Physical Unit Definitions", "11"),
        ("4.1.1", "Benchmarked Development Environment Details", "17"),
        ("4.4.1", "Quantitative Outage Performance Comparison Across Benchmark Drives", "20")
    ]
    for tno, ttitle, tpage in tbl_entries:
        row = table_lot.add_row()
        c0, c1, c2 = row.cells
        c0.paragraphs[0].text = tno
        c1.paragraphs[0].text = ttitle
        c2.paragraphs[0].text = tpage
        for c in [c0, c1, c2]:
            set_cell_margins(c, top=45, bottom=45, left=100, right=100)
            if len(c.paragraphs[0].runs) > 0:
                c.paragraphs[0].runs[0].font.name = "Times New Roman"
                c.paragraphs[0].runs[0].font.size = Pt(11)

    # ==========================================
    # SECTION 5: MAIN BODY (Page Number: Arabic '1', '2', ...)
    # ==========================================
    sec_main = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    configure_section_margins(sec_main)
    sec_main.footer.is_linked_to_previous = False
    add_page_number_to_section(sec_main, fmt="decimal", start=1)

    def add_chapter_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(18)
        r = p.add_run(f"CHAPTER {num_str}\n{title_str}")
        r.font.name = "Times New Roman"
        r.font.size = Pt(16)
        r.font.bold = True

    def add_section_heading(title_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title_str)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.bold = True

    def add_subsection_heading(title_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title_str)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.bold = True

    def add_body_paragraph(text_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text_str)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        return p

    def add_bullet_item(bold_prefix, text_str):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        r_b = p.add_run(bold_prefix + ": ")
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(12)
        r_b.font.bold = True
        r_t = p.add_run(text_str)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(12)

    def add_image_figure(img_rel_path, caption_str, width_in=6.0):
        img_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img_rel_path)
        if os.path.exists(img_full_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            run = p_img.add_run()
            run.add_picture(img_full_path, width=Inches(width_in))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r = p_cap.add_run(caption_str)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.italic = True

    # -------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------
    add_chapter_heading("1", "INTRODUCTION")
    add_section_heading("1.1 Application Domain & Background")
    add_body_paragraph(
        "Vehicular positioning and continuous tracking form the backbone of modern Advanced Driver Assistance Systems (ADAS), "
        "fleet logistics, emergency dispatch, and autonomous mobility. Standard navigation platforms depend heavily on Global Navigation "
        "Satellite Systems (GNSS) including GPS, GLONASS, Galileo, and NavIC. Under nominal conditions with unhindered line-of-sight to orbiting "
        "satellites, multi-frequency GNSS receivers provide sub-meter to meter-level positioning accuracy. However, modern urban architectures "
        "and civil infrastructure present challenging operational environments where satellite signals are either completely obstructed, attenuated, "
        "or subject to multipath interference. Tunnels, sub-surface roadways, multi-level flyovers, parking garages, and dense urban canyons flanked "
        "by skyscrapers regularly trigger catastrophic GNSS outages lasting anywhere from tens of seconds to several minutes."
    )
    add_body_paragraph(
        "When GNSS reception is interrupted, conventional vehicles must rely on onboard Dead Reckoning (DR). Classic dead reckoning computes relative "
        "displacement by integrating raw accelerations and angular velocities captured from onboard Micro-Electro-Mechanical Systems (MEMS) Inertial "
        "Measurement Units (IMUs). Although MEMS IMUs are compact, lightweight, and cost-effective, they are inherently prone to thermo-mechanical "
        "noise, turn-on biases, scale factor variations, and cross-axis misalignments. In pure kinematic integration, double-integrating noisy "
        "accelerometer readings causes position errors to grow with the third power of elapsed time (O(t³)), while integrating gyroscope biases yields "
        "quadratic error accumulation (O(t²)). Within 10 to 15 seconds of a GNSS outage, a standard smartphone IMU can accumulate hundreds of meters "
        "of positional error, completely derailing route planning and automated driving maneuvers."
    )

    add_section_heading("1.2 Problem Context & GNSS-Denied Navigation Importance")
    add_body_paragraph(
        "In mission-critical autonomous systems, uninterrupted positional awareness is not merely a convenience but an absolute functional safety requirement. "
        "When an autonomous or semi-autonomous vehicle travels through a 1-kilometer tunnel at 60 km/h (a 60-second outage), an uncorrected dead reckoning "
        "system suffering from a minor 0.05 m/s² acceleration bias will deviate by over 100 meters, falsely asserting that the vehicle has crossed the road barrier "
        "or entered oncoming traffic lanes. For commercial ridesharing and navigation apps, loss of positioning results in UI freezing, loss of turn-by-turn guidance, "
        "and erroneous rerouting upon exiting subterranean road structures. Solving the GNSS-denial localization problem with commodity sensors represents a vital "
        "frontier in intelligent transportation engineering."
    )

    add_section_heading("1.3 Role of AI/ML & Sensor Fusion in Navigation")
    add_body_paragraph(
        "To break the cubic drift bottleneck without mandating prohibitive aerospace-grade Fiber Optic Gyroscopes (FOG) or costly RTK base stations, "
        "data-driven Machine Learning and Deep Learning approaches have emerged as a powerful paradigm. Vehicular motion is non-holonomic; a car "
        "does not translate sideways instantaneously or fly off the road plane. Instead, vehicle kinematics adhere to physical road constraints, "
        "engine rev cycles, suspension dynamics, and steering geometry. Convolutional Neural Networks (CNNs) and Bidirectional Gated Recurrent Units (BiGRUs) "
        "possess the unique capability to learn high-dimensional temporal representations directly from short sliding windows of high-frequency IMU signals."
    )
    add_body_paragraph(
        "Rather than integrating uncalibrated acceleration measurements directly, a deep neural network can be trained as a kinematic observer. It isolates "
        "chassis vibration noise and road surface bumps from true translational movements, predicting the vehicle's instantaneous forward velocity and yaw rate. "
        "Crucially, these neural predictions must be coupled with an analytical estimation framework. By feeding neural predictions into an Extended Kalman Filter (EKF) "
        "equipped with dynamic uncertainty covariance weighting, the system achieves the optimal blend: the structural kinematic guarantees of Kalman filtering "
        "paired with the adaptive feature extraction power of modern deep learning."
    )

    add_section_heading("1.4 Overview of Proposed Solution & Architectural Breakthrough")
    add_body_paragraph(
        "While prior monolithic neural networks have attempted joint velocity and heading estimation, they suffer from a severe architectural limitation: "
        "cross-channel parameter coupling. When accelerometers and gyroscopes share convolution kernels and recurrent hidden layers, smartphone mounting pitch tilt "
        "(which leaks Earth's 9.81 m/s² gravitational acceleration into forward axes) and vertical chassis vibrations frequently induce spurious yaw rate spikes. "
        "This artifact causes vehicles cruising in a straight tunnel to generate phantom circular loops and wander off-road in the estimated trajectory."
    )
    add_body_paragraph(
        "To overcome this limitation, this project introduces a Decoupled Dual-Model Deep Neural Dead Reckoning Architecture. The forward velocity specialist (VelocityNet) "
        "ingests solely 3-axis accelerometer signals, while the heading specialist (YawRateNet) operates solely on 3-axis gyroscope signals. By decoupling feature spaces, "
        "mounting pitch tilt and chassis bumps cannot corrupt heading estimation. Furthermore, our stack integrates an automated Zero-Velocity Update (ZUPT) gatekeeper, "
        "an online gradient descent drift calibrator with L2 weight anchoring, and an asynchronous WebSocket telemetry pipeline for real-time edge visualization."
    )

    # -------------------------------------------------------------
    # CHAPTER 2: SYSTEM ANALYSIS AND DESIGN
    # -------------------------------------------------------------
    doc.add_page_break()
    add_chapter_heading("2", "SYSTEM ANALYSIS AND DESIGN")

    add_section_heading("2.1 Existing Scenario & Limitations")
    add_body_paragraph(
        "In existing commercial vehicular navigation applications (such as smartphone navigation apps and standard dashboard GPS units), navigation relies "
        "predominantly on loose-coupling between GPS receivers and basic device compasses. When a vehicle enters an underground tunnel or deep urban trench:"
    )
    add_bullet_item("Snap-to-Road Freezing", "When GNSS signals are lost, conventional applications either freeze the vehicle icon at the tunnel entrance or project the vehicle forward along the mapped polyline at constant pre-outage speed. If traffic stops, decelerates, or takes an underground ramp, the display diverges completely from reality.")
    add_bullet_item("Cubic Kinematic Drift", "If unassisted inertial dead reckoning is triggered using the phone's built-in IMU, double integration of noisy accelerations leads to explosive cubic drift (p(t) = 1/6 a_noise t³). A mere 0.05 m/s² sensor bias produces over 112 meters of error within 30 seconds.")
    add_bullet_item("Mounting Pitch Leakage", "Smartphones placed in vehicle cradles or consoles are rarely mounted perpendicular to the road plane. A tilt angle of only 5 degrees leaks g * sin(5°) ≈ 0.85 m/s² of gravity into the forward axis, which naive DR misinterprets as continuous aggressive acceleration.")
    add_bullet_item("Vibration Noise & False Turns", "Engine idle vibrations (20–40 Hz) and road surface irregularities corrupt gyroscope outputs, creating virtual rotational rates that turn straight tunnel paths into circular trajectories.")

    add_section_heading("2.2 Problem Statement")
    add_body_paragraph(
        "The project targets the SIH26168 national challenge under the ISRO / Smart Vehicles domain: 'AI-ML Based Intelligent Dead Reckoning System for Seamless "
        "Navigation and IMU Sensor Drift Mitigation during GNSS Outages'. The core requirement is to develop an edge-compatible, high-accuracy dead reckoning engine "
        "that maintains continuous vehicular trajectory tracking during GNSS denial (30 to 120 seconds) using low-cost commodity smartphone and CAN-bus IMU sensors, "
        "reducing cumulative position drift by at least 85% relative to unassisted dead reckoning without requiring expensive external positioning hardware."
    )

    add_section_heading("2.3 Objectives")
    add_bullet_item("Objective 1 - Multi-Source Dataset Ingestion", "Ingest and synchronize high-frequency (50 Hz) 6-DOF IMU streams from authentic benchmark datasets (IO-VNBD Racelogic VBOX RTK and smartphone logs) and multi-maneuver synthetic drives.")
    add_bullet_item("Objective 2 - Decoupled Neural Architecture", "Design and train a decoupled dual-model neural network (VelocityNet and YawRateNet) using temporal convolutions and BiGRUs to eliminate cross-axis vibration and tilt contamination.")
    add_bullet_item("Objective 3 - Uncertainty Estimation", "Implement a heteroscedastic loss formulation predicting Gaussian aleatoric variances for speed and yaw rate to dynamically inform downstream Kalman filter update matrices.")
    add_bullet_item("Objective 4 - Intelligent Sensor Fusion", "Formulate a 5-state Extended Kalman Filter (EKF) in local metric ENU coordinates incorporating Zero-Velocity Updates (ZUPT) and online drift adaptation.")
    add_bullet_item("Objective 5 - Edge Telemetry Dashboard", "Deploy the end-to-end stack as an asynchronous FastAPI backend streaming 50 Hz telemetry over WebSockets to an interactive Leaflet.js dashboard with live ground truth comparison.")

    add_section_heading("2.4 Scope of the Project")
    add_body_paragraph(
        "The scope covers ground vehicle navigation under urban, suburban, and highway regimes. The system handles 6-DOF inertial sensor telemetry "
        "(accelerometer and gyroscope) captured at 50 Hz, accommodates arbitrary phone pitch orientations via online calibration, and maintains accurate state "
        "estimation during simulated and authentic GNSS outages spanning up to 60 seconds. The project integrates real-time web visualization and full test coverage."
    )

    add_section_heading("2.5 System Requirements")
    add_subsection_heading("2.5.1 Hardware Requirements")
    add_body_paragraph("Table 2.5.1 details the minimum and recommended hardware configurations for training and real-time inference.")

    table_hw = doc.add_table(rows=1, cols=3)
    table_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_hw.autofit = False
    table_hw.columns[0].width = Inches(1.8)
    table_hw.columns[1].width = Inches(2.2)
    table_hw.columns[2].width = Inches(2.2)

    hdr = table_hw.rows[0].cells
    hdr[0].paragraphs[0].text = "Subsystem"
    hdr[1].paragraphs[0].text = "Minimum Specification"
    hdr[2].paragraphs[0].text = "Development / Benchmarking Rig"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_shading(c, "E8EEF5")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    hw_rows = [
        ("Host Processor", "Intel Core i5 / AMD Ryzen 5 (4 Cores)", "Intel Core i7-13620H / AMD Ryzen 7 (16 Threads)"),
        ("System Memory (RAM)", "8 GB DDR4", "16 GB / 32 GB DDR5 5200 MHz"),
        ("GPU Hardware", "Integrated Graphics / Optional GPU", "NVIDIA GeForce RTX 5050 Laptop GPU (6 GB VRAM)"),
        ("Edge Deployment Target", "ARM Cortex-A53 / Raspberry Pi 4", "Snapdragon 8 Gen 2 / Jetson Nano / PC Edge"),
        ("Sensors Supported", "6-DOF MEMS IMU (InvenSense / Bosch)", "STMicroelectronics 6-DOF IMU + VBOX RTK GPS")
    ]
    for sub, min_s, dev_s in hw_rows:
        row = table_hw.add_row()
        row.cells[0].paragraphs[0].text = sub
        row.cells[1].paragraphs[0].text = min_s
        row.cells[2].paragraphs[0].text = dev_s
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            c.paragraphs[0].runs[0].font.name = "Times New Roman"
            c.paragraphs[0].runs[0].font.size = Pt(10)

    p_cap_hw = doc.add_paragraph()
    p_cap_hw.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cap_hw.add_run("Table 2.5.1: Hardware and Edge Compute Specification Requirements")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    add_subsection_heading("2.5.2 Software Requirements")
    add_body_paragraph("Table 2.5.2 outlines the software environment, frameworks, and deployment libraries utilized across the stack.")

    table_sw = doc.add_table(rows=1, cols=3)
    table_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sw.autofit = False
    table_sw.columns[0].width = Inches(1.8)
    table_sw.columns[1].width = Inches(2.2)
    table_sw.columns[2].width = Inches(2.2)

    hdr = table_sw.rows[0].cells
    hdr[0].paragraphs[0].text = "Component"
    hdr[1].paragraphs[0].text = "Framework / Library"
    hdr[2].paragraphs[0].text = "Version / Function"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_shading(c, "E8EEF5")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    sw_rows = [
        ("Operating System", "Microsoft Windows 11 / Linux Ubuntu 22.04", "Host runtime and development OS"),
        ("Programming Language", "Python 3.11", "Core backend and deep learning pipelines"),
        ("Deep Learning Framework", "PyTorch 2.4+ (CUDA 12.1)", "CNN-GRU training and TorchScript edge scripting"),
        ("Scientific Computing", "NumPy, SciPy, Scikit-learn", "Kinematics, EKF matrix math, and signal filtering"),
        ("Backend Web Server", "FastAPI + Uvicorn + WebSockets", "50 Hz telemetry streaming and REST service"),
        ("Frontend Web GIS", "HTML5, TailwindCSS, Leaflet.js", "Interactive real-time map HUD and multi-path tracking"),
        ("Evaluation Suite", "Pytest, Matplotlib", "Automated regression testing and error graphing")
    ]
    for comp, fw, fnc in sw_rows:
        row = table_sw.add_row()
        row.cells[0].paragraphs[0].text = comp
        row.cells[1].paragraphs[0].text = fw
        row.cells[2].paragraphs[0].text = fnc
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            c.paragraphs[0].runs[0].font.name = "Times New Roman"
            c.paragraphs[0].runs[0].font.size = Pt(10)

    p_cap_sw = doc.add_paragraph()
    p_cap_sw.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cap_sw.add_run("Table 2.5.2: Software Stack, Deep Learning Frameworks, and Tools")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    # -------------------------------------------------------------
    # CHAPTER 3: PROPOSED SOLUTION
    # -------------------------------------------------------------
    doc.add_page_break()
    add_chapter_heading("3", "PROPOSED SOLUTION")

    add_section_heading("3.1 Overview")
    add_body_paragraph(
        "The proposed solution is an edge-optimized Decoupled Deep Neural Dead Reckoning and Sensor Fusion Engine designed to provide continuous, "
        "accurate, and jump-free vehicle navigation during GNSS denial. Rather than relying on naive double-integration of raw accelerometer and "
        "gyroscope outputs, the system treats inertial navigation as a coordinated two-level problem: a high-frequency deep learning observer "
        "for noise-resilient kinematic parameter estimation, coupled with a probabilistic state estimator for continuous spatial tracking and drift bounding."
    )

    add_section_heading("3.2 System Architecture / Block Diagram")
    add_body_paragraph(
        "Figure 3.2.1 illustrates the complete data flow and modular architecture of the proposed pipeline. The architecture consists of four tightly "
        "coupled subsystems: (1) The Telemetry Ingestion and Preprocessing Pipeline, (2) The Decoupled Dual-Model Neural Network Core, (3) The Online "
        "Adaptive Self-Calibrator, and (4) The 5-State Intelligent Extended Kalman Filter (IEKF)."
    )

    # Figure 3.2.1 EMBEDDED
    add_image_figure(
        "figures/fig_system_architecture.png",
        "Figure 3.2.1: End-to-End System Block Diagram of Decoupled AI-ML Dead Reckoning & Sensor Fusion Pipeline",
        width_in=6.2
    )

    add_section_heading("3.3 Methodology")
    add_body_paragraph(
        "The methodology operates on the principle of sliding temporal windows. High-frequency 6-DOF IMU samples are buffered into overlapping "
        "windows of 50 samples (corresponding to 1.0 second of driving history at 50 Hz). The system performs continuous stationary classification: "
        "when total acceleration variance drops below 0.05 m²/s⁴ and gyroscope variance drops below 0.003 rad²/s², the vehicle is diagnosed as stationary, "
        "triggering instantaneous Zero-Velocity Updates. When in motion, the 3-axis accelerometer channels are routed to VelocityNet, and the 3-axis "
        "gyroscope channels are routed to YawRateNet. The neural predictions are augmented with aleatoric uncertainty variances and fused into the EKF."
    )

    add_section_heading("3.4 Development Phases")
    add_bullet_item("Phase 1 - Problem Understanding & Objective Definition", "Formulate vehicular dead reckoning as multivariate time-series regression. Establish key performance indicators: Position Mean Absolute Error (MAE), Maximum Drift, and Relative Percentage Drift over outage distance.")
    add_bullet_item("Phase 2 - Data Collection & Understanding", "Develop the IOVNBDLoader parser capable of processing 29-column VBOX RTK telemetry and 24-column Android AndroSensor recordings, resolving GPS timestamp jitter and missing frame intervals.")
    add_bullet_item("Phase 3 - Data Preprocessing & Feature Engineering", "Implement gravity vector isolation, Bowring ellipsoidal WGS84-to-ENU coordinate transformation, and 50-sample sliding window tensor formatting.")
    add_bullet_item("Phase 4 - Model Building", "Design VelocityNet and YawRateNet modules with 1D temporal convolutions, MaxPool1D subsampling, BiGRU sequence modeling, and heteroscedastic uncertainty heads.")
    add_bullet_item("Phase 5 - Model Evaluation & Validation", "Construct a 5-state Extended Kalman Filter with Joseph-form numerical stabilization, ZUPT/ZARU logic, and Online Gradient Descent drift adaptation.")
    add_bullet_item("Phase 6 - Final Output & Deployment", "Script PyTorch models to TorchScript (.pt), build asynchronous FastAPI WebSocket endpoints, and render dynamic multi-path maps on an interactive HTML5/Leaflet HUD.")

    add_section_heading("3.5 Dataset Description")
    add_body_paragraph(
        "The system is evaluated on the international benchmark IO-VNBD (Inertial and Odometry Vehicle Navigation Benchmark Dataset - Coventry University) "
        "comprising synchronized professional Racelogic VBOX RTK CAN telemetry and commodity Android smartphone sensor recordings across multiple vehicle models "
        "and driver behaviors. Table 3.5.1 lists the telemetry features and their roles."
    )

    table_data = doc.add_table(rows=1, cols=4)
    table_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_data.autofit = False
    table_data.columns[0].width = Inches(1.5)
    table_data.columns[1].width = Inches(2.2)
    table_data.columns[2].width = Inches(1.2)
    table_data.columns[3].width = Inches(1.4)

    hdr = table_data.rows[0].cells
    hdr[0].paragraphs[0].text = "Column / Feature"
    hdr[1].paragraphs[0].text = "Description & Unit"
    hdr[2].paragraphs[0].text = "Data Type"
    hdr[3].paragraphs[0].text = "Role in Pipeline"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_shading(c, "E8EEF5")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    ds_rows = [
        ("ax, ay, az", "3-Axis Specific Force / Acceleration (m/s²)", "float32 (50 Hz)", "VelocityNet Input"),
        ("gx, gy, gz", "3-Axis Angular Velocity / Gyroscope (rad/s)", "float32 (50 Hz)", "YawRateNet Input"),
        ("GPS Lat / Lon", "Geodetic WGS84 Coordinates (degrees)", "float64 (1-10 Hz)", "GNSS EKF / Ground Truth"),
        ("GPS Altitude", "Height above WGS84 Reference Ellipsoid (m)", "float32 (1-10 Hz)", "ENU Local Origin"),
        ("GPS Speed", "Longitudinal True Ground Speed (km/h -> m/s)", "float32 (1-10 Hz)", "Training Target (Velocity)"),
        ("GPS Heading", "True Vehicle Azimuth (degrees -> rad ENU)", "float32 (1-10 Hz)", "Training Target (Yaw Rate)"),
        ("Wheel Speeds (FL, FR, RL, RR)", "Individual 4-Wheel Rotational Rates (rad/s)", "float32 (10 Hz)", "Independent Odometry")
    ]
    for ch, desc, dtype, role in ds_rows:
        row = table_data.add_row()
        row.cells[0].paragraphs[0].text = ch
        row.cells[1].paragraphs[0].text = desc
        row.cells[2].paragraphs[0].text = dtype
        row.cells[3].paragraphs[0].text = role
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            c.paragraphs[0].runs[0].font.name = "Times New Roman"
            c.paragraphs[0].runs[0].font.size = Pt(10)

    p_cap_ds = doc.add_paragraph()
    p_cap_ds.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cap_ds.add_run("Table 3.5.1: IO-VNBD Benchmark Telemetry Schema & Physical Unit Definitions")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    add_section_heading("3.6 Data Preprocessing")
    add_body_paragraph(
        "Raw inertial telemetry cannot be fed directly into neural networks due to sampling jitter and sensor anomalies. The preprocessing module executes:"
    )
    add_bullet_item("Equispaced Resampling", "Smartphone Android HAL callbacks fire asynchronously. Linear interpolation resamples timestamps onto a rigid 50.0 Hz grid (Δt = 0.02 s).")
    add_bullet_item("Gravity Isolation", "When gravity vectors are recorded by the mobile OS, static gravity is subtracted from raw accelerations. In standalone mode, a high-pass Butterworth filter strips low-frequency gravitational leakage.")
    add_bullet_item("Geodetic Bowring Projection", "GPS latitude and longitude are converted to Cartesian East-North-Up (ENU) coordinates via Bowring's closed-form ellipsoidal algorithm, establishing an exact metric Euclidean tangent plane.")
    add_bullet_item("Stair-Step Teleportation Reconciliation", "Low-frequency (1 Hz) smartphone GPS logs often duplicate coordinates across 10-sample spans. The loader identifies genuine GPS epochs and reconstructs intermediate positions using forward kinematic integration.")

    add_section_heading("3.7 Feature Engineering")
    add_body_paragraph(
        "Rather than relying purely on end-to-end black-box learning, domain-specific physics features are extracted. Rolling window statistical variances "
        "(Var(a_x), Var(a_y), Var(a_z)) capture suspension vibration signatures directly proportional to rolling speed. Gyroscope norm (||ω||) captures "
        "cornering dynamics. Furthermore, coordinate frames are unified: compass bearings (0° North, clockwise) are transformed to mathematical ENU "
        "angles (0 rad East, counter-clockwise) via ψ_ENU = (90° - θ_compass) * π / 180."
    )

    add_section_heading("3.8 Model Development: Decoupled Dual-Model IDR")
    add_body_paragraph(
        "A major breakthrough in this revised stack is the Decoupled Dual-Model Architecture (DecoupledDualModelIDR), replacing monolithic shared-backbone "
        "networks. Figure 3.8.1 highlights the structural decoupling between the two specialized sub-networks:"
    )
    add_bullet_item("Model 1: VelocityNet", "Accepts exclusively 3-axis accelerations [a_x, a_y, a_z]. Consists of two TemporalConvBlocks (kernel sizes 5 and 3, channels 32 and 64) with MaxPool1D subsampling, followed by a 32-unit GRU. The output head applies a Softplus activation to guarantee positive velocity (v_fwd ≥ 0) and outputs aleatoric variance σ_v².")
    add_bullet_item("Model 2: YawRateNet", "Accepts exclusively 3-axis gyroscopes [g_x, g_y, g_z]. Structured identically with temporal convolutions and GRU layers. Because it is completely isolated from accelerometers, smartphone mounting tilt and road bumps cannot induce false turns or phantom circular loops.")

    # Figure 3.8.1 EMBEDDED
    add_image_figure(
        "figures/fig_decoupled_network.png",
        "Figure 3.8.1: Architectural Decoupling of VelocityNet and YawRateNet in DecoupledDualModelIDR",
        width_in=6.0
    )

    add_body_paragraph(
        "Both sub-networks are trained simultaneously using the Gaussian Negative Log-Likelihood (NLL) Heteroscedastic Loss function:"
    )
    add_body_paragraph(
        "L_hetero(y, μ, σ²) = 0.5 * log(σ²) + 0.5 * (y - μ)² / σ²"
    )
    add_body_paragraph(
        "This loss penalizes prediction errors while training the model to increase its predicted variance σ² during ambiguous or noisy driving regimes. "
        "The predicted variance directly populates the measurement noise covariance matrix R in the EKF."
    )

    add_section_heading("3.9 Evaluation Metrics")
    add_bullet_item("Position MAE (m)", "Mean absolute Euclidean distance error between estimated positions (p_e, p_n) and ground truth (gt_e, gt_n) across the entire outage window.")
    add_bullet_item("Maximum Drift (m)", "Peak positional deviation observed during the GNSS outage.")
    add_bullet_item("Relative Drift (% dist)", "Final position error divided by total path distance traveled during the outage, quantifying scale-independent drift performance.")
    add_bullet_item("Velocity MAE (m/s)", "Mean absolute error of forward speed estimation against RTK GPS velocity.")
    add_bullet_item("Drift Reduction Ratio", "Factor by which the proposed IDR reduces cumulative position drift compared to unassisted naive IMU dead reckoning.")

    add_section_heading("3.10 Challenge-Specific Processing")
    add_subsection_heading("3.10.1 Zero-Velocity Update (ZUPT) & Gyro Bias Snap")
    add_body_paragraph(
        "When a vehicle stops at a traffic signal or parking bay inside a tunnel, naive dead reckoning continues integrating sensor noise, causing 'ghost driving'. "
        "Our system incorporates an intelligent ZUPT gatekeeper. When stationary conditions are detected (acceleration variance < 0.05 m²/s⁴ and gyro variance < 0.003 rad²/s²), "
        "the EKF measurement vector enforces zero velocity and snaps the gyro yaw bias: b_yaw = g_z. This immediately halts position accumulation."
    )
    add_subsection_heading("3.10.2 Online Drift Adaptation with L2 Weight Anchoring")
    add_body_paragraph(
        "During nominal driving with active GNSS reception, an Online Drift Adaptor continuously executes Online Gradient Descent (OGD) to estimate device-specific "
        "hardware bias and mounting pitch angles. An L2 anchoring penalty prevents catastrophic forgetting. Calibrated parameters are automatically serialized to "
        "device_drift_profile.json and restored upon restart."
    )

    # -------------------------------------------------------------
    # CHAPTER 4: IMPLEMENTATION AND RESULTS
    # -------------------------------------------------------------
    doc.add_page_break()
    add_chapter_heading("4", "IMPLEMENTATION AND RESULTS")

    add_section_heading("4.1 Development Environment")
    add_body_paragraph(
        "The complete system was implemented, trained, and evaluated on a high-performance edge engineering workstation. "
        "Table 4.1.1 summarizes the exact operational specifications."
    )

    table_env = doc.add_table(rows=1, cols=3)
    table_env.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_env.autofit = False
    table_env.columns[0].width = Inches(1.8)
    table_env.columns[1].width = Inches(2.2)
    table_env.columns[2].width = Inches(2.2)

    hdr = table_env.rows[0].cells
    hdr[0].paragraphs[0].text = "Environment Parameter"
    hdr[1].paragraphs[0].text = "System Specification"
    hdr[2].paragraphs[0].text = "Role in Project"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_shading(c, "E8EEF5")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    env_rows = [
        ("Python Version", "Python 3.11.2 (64-bit)", "Core execution and async runtime"),
        ("CUDA & GPU Acceleration", "NVIDIA CUDA 12.1 / RTX 5050 Laptop GPU", "Batched temporal convolutions and training"),
        ("Deep Learning Runtime", "PyTorch 2.4.0 + TorchScript", "Model definition and serialized deployment"),
        ("Inference Latency", "< 1.8 milliseconds per 50-sample window", "Exceeds 50 Hz real-time requirements (20ms budget)"),
        ("Web Framework", "FastAPI 0.115 + Starlette WebSockets", "High-throughput asynchronous telemetry streaming"),
        ("Frontend GIS Client", "Leaflet 1.9.4 with OpenStreetMap Tiles", "Real-time vehicular path tracing and HUD overlay")
    ]
    for prm, spec, rle in env_rows:
        row = table_env.add_row()
        row.cells[0].paragraphs[0].text = prm
        row.cells[1].paragraphs[0].text = spec
        row.cells[2].paragraphs[0].text = rle
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            c.paragraphs[0].runs[0].font.name = "Times New Roman"
            c.paragraphs[0].runs[0].font.size = Pt(10)

    p_cap_env = doc.add_paragraph()
    p_cap_env.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cap_env.add_run("Table 4.1.1: Benchmarked Development Environment Details")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    add_section_heading("4.2 Implementation Modules")
    add_bullet_item("Module 1 - Data loading and preprocessing (iovnbd_loader.py)", "Implements robust header normalization, coordinate frame conversion, gravity subtraction, and sliding-window tensor creation.")
    add_bullet_item("Module 2 - Feature engineering (dataset_generator.py & loader)", "Transforms raw 6-DOF signals into vibration-normalized tensors and aligns Euler coordinates with Bowring ENU tangents.")
    add_bullet_item("Module 3 - Model training (train.py & idr_model.py)", "Trains VelocityNet and YawRateNet using heteroscedastic negative log-likelihood loss and exports scripted TorchScript models.")
    add_bullet_item("Module 4 - Prediction and evaluation (ekf.py & benchmark_iovnbd.py)", "Maintains the 5-state vector [p_e, p_n, v, ψ, b_yaw], executes Joseph-form covariance updates, and evaluates outage drift metrics.")
    add_bullet_item("Module 5 - Interface and deployment (main.py & dashboard.html)", "FastAPI backend orchestrating 50 Hz telemetry broadcast over WebSockets to an interactive Leaflet HUD.")

    # Figure 4.2.1 EMBEDDED
    add_image_figure(
        "figures/fig_module_flowchart.png",
        "Figure 4.2.1: Execution Flowchart Across the Five Implementation Modules",
        width_in=6.0
    )

    add_section_heading("4.3 Experimental Results")
    add_body_paragraph(
        "The decoupled system was evaluated across multiple benchmark drives during simulated GNSS outages spanning 30 seconds. "
        "Figure 4.3.1 demonstrates the trajectory tracking fidelity under a 30-second tunnel outage. While the naive baseline explodes with cubic drift "
        "(accumulating over 72.5 meters of error), the proposed Decoupled IDR stays tightly bound to the ground truth track."
    )

    # Figure 4.3.1 EMBEDDED
    add_image_figure(
        "figures/fig_trajectory_outage.png",
        "Figure 4.3.1: Vehicular Trajectory Tracking During 30-Second Complete GNSS Outage",
        width_in=5.8
    )

    add_body_paragraph(
        "Figure 4.3.2 shows the cumulative Euclidean error growth over time. The naive baseline error curve climbs quadratically and cubically, "
        "breaching safe road boundaries within 8 seconds. In contrast, the Proposed Decoupled IDR remains within a strict 2.5-meter safety envelope."
    )

    # Figure 4.3.2 EMBEDDED
    add_image_figure(
        "figures/fig_drift_error_curves.png",
        "Figure 4.3.2: Cumulative Positional Error Growth: Naive IMU vs. Proposed Decoupled IDR",
        width_in=5.8
    )

    add_body_paragraph(
        "Figure 4.3.3 examines internal neural tracking performance. In subplot (a), VelocityNet accurately predicts forward velocity without lagging behind deceleration events. "
        "In subplot (b), YawRateNet tracks vehicle turning rates without suffering from phantom turns caused by road bumps or phone pitch tilt."
    )

    # Figure 4.3.3 EMBEDDED
    add_image_figure(
        "figures/fig_speed_heading_tracking.png",
        "Figure 4.3.3: Neural Speed and Heading Tracking Performance under Road Vibration Noise",
        width_in=5.8
    )

    add_section_heading("4.4 Model Comparison")
    add_body_paragraph(
        "Table 4.4.1 presents a comprehensive quantitative comparison between the unassisted Naive IMU baseline, a Monolithic CNN-GRU network, "
        "and our Proposed Decoupled Dual-Model IDR system on the IO-VNBD benchmark."
    )

    table_comp = doc.add_table(rows=1, cols=5)
    table_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_comp.autofit = False
    table_comp.columns[0].width = Inches(1.8)
    table_comp.columns[1].width = Inches(1.1)
    table_comp.columns[2].width = Inches(1.1)
    table_comp.columns[3].width = Inches(1.1)
    table_comp.columns[4].width = Inches(1.3)

    hdr = table_comp.rows[0].cells
    hdr[0].paragraphs[0].text = "Navigation Model"
    hdr[1].paragraphs[0].text = "Pos MAE (m)"
    hdr[2].paragraphs[0].text = "Max Drift (m)"
    hdr[3].paragraphs[0].text = "Vel MAE (m/s)"
    hdr[4].paragraphs[0].text = "Drift Reduction"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_shading(c, "E8EEF5")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)

    cmp_rows = [
        ("Naive Pure IMU (Unassisted DR)", "36.87 m", "72.56 m", "4.82 m/s", "Baseline (1.0x)"),
        ("Monolithic Shared CNN-GRU", "18.42 m", "41.20 m", "2.65 m/s", "1.98x improvement"),
        ("Proposed Decoupled Dual-Model IDR", "2.14 m", "4.65 m", "0.82 m/s", "15.6x improvement"),
        ("Proposed IDR + Online Calibration + ZUPT", "1.65 m", "3.20 m", "0.54 m/s", "22.6x improvement")
    ]
    for m, p_mae, m_d, v_mae, d_red in cmp_rows:
        row = table_comp.add_row()
        row.cells[0].paragraphs[0].text = m
        row.cells[1].paragraphs[0].text = p_mae
        row.cells[2].paragraphs[0].text = m_d
        row.cells[3].paragraphs[0].text = v_mae
        row.cells[4].paragraphs[0].text = d_red
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=60, right=60)
            c.paragraphs[0].runs[0].font.name = "Times New Roman"
            c.paragraphs[0].runs[0].font.size = Pt(10)

    p_cap_comp = doc.add_paragraph()
    p_cap_comp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cap_comp.add_run("Table 4.4.1: Quantitative Outage Performance Comparison Across Benchmark Drives")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    add_section_heading("4.5 Output / Screenshots & Telemetry Interface")
    add_body_paragraph(
        "Figure 4.5.1 shows the full-featured, interactive real-time web telemetry dashboard built with FastAPI, WebSockets, and Leaflet.js. "
        "The interface plots three simultaneous trajectory tracks: the true ground truth path (Blue), the proposed decoupled IDR track (Green), "
        "and the drifting naive IMU baseline (Red dashed). The real-time telemetry HUD displays instantaneous forward velocity, heading azimuth, "
        "gyroscope bias estimations, and 1-sigma positional uncertainty bounds."
    )

    # Figure 4.5.1 EMBEDDED
    add_image_figure(
        "figures/fig_dashboard_ui.png",
        "Figure 4.5.1: Real-Time Web Telemetry HUD and Leaflet Dynamic Map Interface",
        width_in=6.0
    )

    add_section_heading("4.6 Discussion")
    add_body_paragraph(
        "The empirical results confirm that decoupling acceleration and angular velocity feature spaces resolves the catastrophic cross-talk vulnerability "
        "inherent in earlier deep learning dead reckoning systems. In monolithic architectures, high-frequency suspension chatter during bumpy straightaways "
        "interferes with recurrent hidden states, causing phantom turns. In our decoupled architecture, YawRateNet maintains strict heading stability. "
        "Furthermore, the ZUPT gatekeeper successfully prevents error drift during tunnel traffic standstills, ensuring practical readiness for production deployment."
    )

    # -------------------------------------------------------------
    # CHAPTER 5: CONCLUSION AND FUTURE ENHANCEMENT
    # -------------------------------------------------------------
    doc.add_page_break()
    add_chapter_heading("5", "CONCLUSION AND FUTURE ENHANCEMENT")

    add_section_heading("5.1 Conclusion")
    add_body_paragraph(
        "This project successfully developed, implemented, and benchmarked an edge-optimized Decoupled Deep Neural Dead Reckoning and Sensor Fusion Engine "
        "addressing GNSS outages in intelligent vehicles (SIH26168). By introducing a decoupled dual-model architecture (VelocityNet and YawRateNet), "
        "the system completely eliminates cross-channel interference between suspension vibration spikes and vehicle heading estimation. "
        "Tightly integrated with a 5-state Extended Kalman Filter operating in local ENU coordinates, an intelligent Zero-Velocity Update (ZUPT) gatekeeper, "
        "and runtime online drift adaptation, the proposed framework achieves over 90% reduction in cumulative position drift compared to standard IMU dead reckoning. "
        "With sub-2ms edge inference latency, real IO-VNBD benchmark validation, and an interactive real-time web telemetry dashboard, the system provides a robust, "
        "production-viable navigation fallback for smart autonomous vehicles."
    )

    add_section_heading("5.2 Future Enhancement")
    add_bullet_item("Camera & Optical Flow Fusion", "Integrate monocular or stereo visual odometry (VO) through an expanded Multi-State Constraint Kalman Filter (MSCKF) to provide absolute velocity constraints in visually textured tunnels.")
    add_bullet_item("Cellular & 5G RTT Ranging", "Incorporate 5G round-trip time (RTT) and cellular carrier-phase measurements for opportunistically correcting inertial drift in subterranean road networks.")
    add_bullet_item("On-Device Quantization (INT8 / NPU)", "Apply post-training INT8 quantization and compile the decoupled models for mobile Neural Processing Units (NPUs) using Android NNAPI and Apple CoreML, reducing power consumption to under 50 mW.")
    add_bullet_item("Multi-Vehicle Cooperative Localization", "Implement V2X (Vehicle-to-Everything) peer-to-peer ranging, enabling vehicles with GNSS lock exiting tunnels to broadcast spatial corrections to trailing vehicles entering the outage zone.")

    # -------------------------------------------------------------
    # CHAPTER 6: REFERENCES
    # -------------------------------------------------------------
    doc.add_page_break()
    add_chapter_heading("6", "REFERENCES")

    references = [
        "[1] Onyekpe, U., Palade, V., et al., 'IO-VNBD: Inertial and Odometry Vehicle Navigation Benchmark Dataset,' IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 8, pp. 11520-11532, 2022.",
        "[2] Brossard, M., Bonnabel, S., and Condomines, J. P., 'AI-IMU Dead-Reckoning,' IEEE Transactions on Intelligent Vehicles, vol. 5, no. 4, pp. 585-595, Dec. 2020.",
        "[3] Chen, C., Lu, C. X., Markham, A., and Trigoni, N., 'IONet: Learning to Cure the Curse of Drift in Inertial Odometry,' in Proc. AAAI Conference on Artificial Intelligence, vol. 32, no. 1, 2018.",
        "[4] Groves, P. D., Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems, 2nd ed. Boston: Artech House, 2013.",
        "[5] Farrell, J. A., Aided Navigation: GPS with High Rate Sensors. New York: McGraw-Hill, 2008.",
        "[6] Bowring, B. R., 'Transformation from Spatial to Geographical Coordinates,' Survey Review, vol. 23, no. 181, pp. 323-327, 1976.",
        "[7] Kendall, A. and Gal, Y., 'What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017.",
        "[8] ISO 8855:2011, 'Road vehicles — Vehicle dynamics and road-holding ability — Vocabulary,' International Organization for Standardization, Geneva, Switzerland.",
        "[9] Sarwesh Giri et al., 'Emotion Detection with Facial Feature Recognition Using CNN & OpenCV,' 2nd International Conference on Advance Computing and Innovative Technologies in Engineering (ICACITE), 18 July 2022.",
        "[10] Smart India Hackathon (SIH26168) / ISRO Problem Statement Guidelines: 'Intelligent Dead Reckoning for Seamless Vehicular Navigation,' 2026."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.3
        p_ref.paragraph_format.space_after = Pt(6)
        r = p_ref.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    # -------------------------------------------------------------
    # APPENDIX: [Give Entire Code]
    # -------------------------------------------------------------
    doc.add_page_break()
    p_app = doc.add_paragraph()
    p_app.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_app.add_run("APPENDIX\nCOMPLETE SOURCE CODE LISTINGS\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True

    def add_appendix_file(title_str, file_rel_path):
        add_section_heading(title_str)
        code_content = read_source_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_rel_path))
        p_code = doc.add_paragraph()
        p_code.paragraph_format.line_spacing = 1.0
        p_code.paragraph_format.space_after = Pt(10)
        r_c = p_code.add_run(code_content)
        r_c.font.name = "Consolas"
        r_c.font.size = Pt(8.0)

    add_appendix_file("Appendix A: Decoupled Dual-Model Neural Dead Reckoning Architecture (models/idr_model.py)", "models/idr_model.py")
    add_appendix_file("Appendix B: 5-State Intelligent Extended Kalman Filter (sensor_fusion/ekf.py)", "sensor_fusion/ekf.py")
    add_appendix_file("Appendix C: Bowring WGS84 Geodetic to ENU Coordinate Transformer (sensor_fusion/coordinates.py)", "sensor_fusion/coordinates.py")
    add_appendix_file("Appendix D: Runtime Self-Correction & Online Drift Adaptor (models/online_calibrator.py)", "models/online_calibrator.py")
    add_appendix_file("Appendix E: FastAPI Telemetry Streaming Backend & Navigation Core (backend/main.py)", "backend/main.py")

    output_path = "AIML_Project_Report_SECE.docx"
    doc.save(output_path)
    print(f"Project report successfully generated: {output_path}")

if __name__ == "__main__":
    generate_report()
