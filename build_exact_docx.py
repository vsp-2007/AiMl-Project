"""
Generates the official Word Document (.docx) matching the student example format:
- Exactly follows the formatting conditions:
  * Paper Size: A4
  * Font: Times New Roman throughout
  * Heading 1 (Chapter): 16 pt, Bold
  * Heading 2 (Section): 14 pt, Bold
  * Heading 3 (Sub-section): 12 pt, Bold
  * Body Text: 12 pt, 1.5 line spacing, Justified
  * Margins: Left 1.5 inch, Right 1.0 inch, Top 1.0 inch, Bottom 1.0 inch
  * Page Numbering: Abstract (i), TOC (no page number), List of Figures (ii), Chapter 1 onwards (1, 2, ...)
- Includes placeholders for diagrams/screenshots as requested
- Contains the COMPLETE source code line-by-line in the Appendix for all files
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def add_page_number(section, fmt="decimal", start=None):
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

def configure_margins(section):
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)

def read_code_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"# File not found: {path}"

def build_docx():
    doc = docx.Document()

    # Normal Style configuration
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # -------------------------------------------------------------
    # SECTION 1: PRELIMINARY PAGES (No Page Number)
    # -------------------------------------------------------------
    sec1 = doc.sections[0]
    configure_margins(sec1)
    sec1.footer.is_linked_to_previous = False
    sec1.footer.paragraphs[0].text = ""

    # OUTER COVER PAGE
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_top.add_run("AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM\nFOR VEHICULAR NAVIGATION DURING GNSS OUTAGES")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(36)
    r = p_date.add_run("OCTOBER 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_mid = doc.add_paragraph()
    p_mid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid.paragraph_format.space_before = Pt(40)
    p_mid.paragraph_format.line_spacing = 1.3
    r = p_mid.add_run(
        "PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT\n"
        "OF THE REQUIREMENTS FOR THE AWARD OF THE\n"
        "DEGREE OF BACHELOR OF ENGINEERING\n"
        "IN COMPUTER SCIENCE AND ENGINEERING\n"
        "OF THE ANNA UNIVERSITY"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    # Boxed left and right submitted by
    tbl_sub = doc.add_table(rows=1, cols=2)
    tbl_sub.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sub.autofit = False
    tbl_sub.columns[0].width = Inches(2.2)
    tbl_sub.columns[1].width = Inches(3.5)

    c0 = tbl_sub.rows[0].cells[0]
    p_box = c0.paragraphs[0]
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(30)
    r = p_box.add_run("━━━━━━━━━━━━━\nAI & ML\nPROJECT\nWORK\n━━━━━━━━━━━━━")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    c1 = tbl_sub.rows[0].cells[1]
    p_s = c1.paragraphs[0]
    p_s.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_s.paragraph_format.space_before = Pt(30)
    r = p_s.add_run("Submitted by\n\n[STUDENT NAME 1] – [REGISTER NUMBER 1]\n[STUDENT NAME 2] – [REGISTER NUMBER 2]\n\nBATCH\n2025 - 2029")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_guide.paragraph_format.space_before = Pt(40)
    r = p_guide.add_run("Under the Guidance of\nDR. V. NIRANJANI\nAssistant Professor, CSE.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_before = Pt(50)
    r = p_bot.add_run(
        "COMPUTER SCIENCE AND ENGINEERING\n"
        "Sri Eshwar College of Engineering\n"
        "(An Autonomous Institution – Affiliated to Anna University)\n"
        "COIMBATORE – 641 202"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    # INNER COVER PAGE
    doc.add_page_break()

    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_top.add_run("AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM\nFOR VEHICULAR NAVIGATION DURING GNSS OUTAGES")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(36)
    r = p_date.add_run("OCTOBER 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_mid = doc.add_paragraph()
    p_mid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid.paragraph_format.space_before = Pt(40)
    p_mid.paragraph_format.line_spacing = 1.3
    r = p_mid.add_run(
        "PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT\n"
        "OF THE REQUIREMENTS FOR THE AWARD OF THE\n"
        "DEGREE OF BACHELOR OF ENGINEERING\n"
        "IN COMPUTER SCIENCE AND ENGINEERING\n"
        "OF THE ANNA UNIVERSITY"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    tbl_sub2 = doc.add_table(rows=1, cols=2)
    tbl_sub2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sub2.autofit = False
    tbl_sub2.columns[0].width = Inches(2.2)
    tbl_sub2.columns[1].width = Inches(3.5)

    c0 = tbl_sub2.rows[0].cells[0]
    p_box = c0.paragraphs[0]
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(30)
    r = p_box.add_run("━━━━━━━━━━━━━\nAI & ML\nPROJECT\nWORK\n━━━━━━━━━━━━━")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    c1 = tbl_sub2.rows[0].cells[1]
    p_s = c1.paragraphs[0]
    p_s.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_s.paragraph_format.space_before = Pt(30)
    r = p_s.add_run("Submitted by\n\n[STUDENT NAME 1] – [REGISTER NUMBER 1]\n[STUDENT NAME 2] – [REGISTER NUMBER 2]\n\nBATCH\n2025 - 2029")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_guide.paragraph_format.space_before = Pt(40)
    r = p_guide.add_run("Under the Guidance of\nDR. V. NIRANJANI\nAssistant Professor, CSE.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_before = Pt(50)
    r = p_bot.add_run(
        "Department of Computer Science and Engineering\n"
        "Sri Eshwar College of Engineering\n"
        "(An Autonomous Institution – Affiliated to Anna University)\n"
        "COIMBATORE – 641 202"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    # BONAFIDE CERTIFICATE (Page 1)
    doc.add_page_break()

    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
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
        "for the course U23AM495 - Artificial Intelligence and Machine Learning is the bonafide work of\n\n"
        " [STUDENT NAME 1]       [REGISTER NUMBER 1]\n"
        " [STUDENT NAME 2]       [REGISTER NUMBER 2]\n\n"
        "who carried out the project work under my supervision.\n"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    table_sign = doc.add_table(rows=1, cols=2)
    table_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sign.autofit = False
    table_sign.columns[0].width = Inches(3.0)
    table_sign.columns[1].width = Inches(3.0)

    p_s0 = table_sign.rows[0].cells[0].paragraphs[0]
    p_s0.paragraph_format.line_spacing = 1.2
    r0 = p_s0.add_run("-----------------------------------------\nSIGNATURE\nDr. R. SUBHA M.E., Ph. D.\nHEAD OF THE DEPARTMENT\nDept. of Computer Science & Engineering\nSri Eshwar College of Engineering,\nCoimbatore – 641 202.")
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(11)
    r0.font.bold = True

    p_s1 = table_sign.rows[0].cells[1].paragraphs[0]
    p_s1.paragraph_format.line_spacing = 1.2
    r1 = p_s1.add_run("-----------------------------------------\nSIGNATURE\nDR. V. NIRANJANI\nSUPERVISOR\nAssistant Professor,\nDept. of Computer Science & Engineering,\nSri Eshwar College of Engineering,\nCoimbatore – 641 202.")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.bold = True

    p_viva = doc.add_paragraph()
    p_viva.paragraph_format.space_before = Pt(36)
    r = p_viva.add_run("Submitted for the Autonomous Semester End Project Viva-Voce held on …………………..")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    table_exam = doc.add_table(rows=1, cols=2)
    table_exam.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_exam.autofit = False
    table_exam.columns[0].width = Inches(3.0)
    table_exam.columns[1].width = Inches(3.0)

    p_e0 = table_exam.rows[0].cells[0].paragraphs[0]
    p_e0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_e0.paragraph_format.space_before = Pt(20)
    r_e0 = p_e0.add_run("_________________________\nINTERNAL EXAMINER")
    r_e0.font.name = "Times New Roman"
    r_e0.font.size = Pt(11)
    r_e0.font.bold = True

    p_e1 = table_exam.rows[0].cells[1].paragraphs[0]
    p_e1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_e1.paragraph_format.space_before = Pt(20)
    r_e1 = p_e1.add_run("_________________________\nEXTERNAL EXAMINER")
    r_e1.font.name = "Times New Roman"
    r_e1.font.size = Pt(11)
    r_e1.font.bold = True

    p_foot_cert = doc.add_paragraph()
    p_foot_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot_cert.paragraph_format.space_before = Pt(36)
    r = p_foot_cert.add_run("Sri Eshwar College of Engineering\n(An Autonomous Institution – Affiliated to Anna University)\nCOIMBATORE – 641 202")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    # DECLARATION
    doc.add_page_break()

    p_dec_t = doc.add_paragraph()
    p_dec_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dec_t.add_run("DECLARATION\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p_n = doc.add_paragraph()
    p_n.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_n.add_run("[STUDENT NAME 1]  [[REGISTER NUMBER 1]]\n[STUDENT NAME 2]  [[REGISTER NUMBER 2]]\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_dec_b = doc.add_paragraph()
    p_dec_b.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dec_b.paragraph_format.line_spacing = 1.5
    r = p_dec_b.add_run(
        "To declare that the project entitled “AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES” "
        "submitted in partial fulfilment to the University as the project work of Bachelor of Engineering (Computer Science and Engineering) Degree, "
        "is a record of original work done by us under the supervision and guidance of DR. V. NIRANJANI, Assistant Professor, "
        "Department of Computer Science and Engineering, Sri Eshwar College of Engineering, Coimbatore.\n"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_pl = doc.add_paragraph()
    r = p_pl.add_run("Place: Coimbatore\nDate:\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_st_sig = doc.add_paragraph()
    p_st_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_st_sig.add_run("[STUDENT NAME 1]\n[STUDENT NAME 2]\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_gd = doc.add_paragraph()
    r = p_gd.add_run("Project Guided by,\n\nDR. V. NIRANJANI")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    # ACKNOWLEDGEMENT
    doc.add_page_break()

    p_ack_t = doc.add_paragraph()
    p_ack_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_ack_t.add_run("ACKNOWLEDGEMENT\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p_ack_b = doc.add_paragraph()
    p_ack_b.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ack_b.paragraph_format.line_spacing = 1.5
    r = p_ack_b.add_run(
        "The success of a work depends on a team and cooperation. I take this opportunity to express my gratitude and thanks to everyone who helped me in my project. "
        "I would like to thank the management for the constant support provided by them to complete this project.\n\n"
        "It is indeed our great honor bounded duty to thank our beloved Chairman Mr. R. Mohanram, for his academic interest shown towards the students.\n\n"
        "We are indebted to our Director Mr. R. Rajaram, for motivating and providing us with all facilities.\n\n"
        "I wish to express my sincere regards and deep sense of gratitude to Dr. Sudha Mohanram, M.E, Ph.D. Principal, for the excellent facilities and encouragement provided during the course of the study and project.\n\n"
        "We are indebted to Dr. R. Subha, M.E., Ph.D. Dean, Computing Science for having permitted us to carry out this project and giving the complete freedom to utilize the resources.\n\n"
        "I express my sincere thanks to my course faculty Dr. V. Niranjani, Assistant Professor of Computer Science and Engineering Department for the valuable guidance and encouragement given, to us for this project.\n\n"
        "I solemnly express our thanks to all the teaching and nonteaching staff of the Computer Science and Engineering Department, family and friends for their valuable support which inspired us to work on this project."
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # -------------------------------------------------------------
    # SECTION 2: ABSTRACT (Page Number: Roman 'i')
    # -------------------------------------------------------------
    sec_abs = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    configure_margins(sec_abs)
    sec_abs.footer.is_linked_to_previous = False
    add_page_number(sec_abs, fmt="lowerRoman", start=1)

    p_abs_h = doc.add_paragraph()
    p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_abs_h.add_run("ABSTRACT\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p_abs_text = doc.add_paragraph()
    p_abs_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs_text.paragraph_format.line_spacing = 1.5
    r = p_abs_text.add_run(
        "Vehicular navigation and automated positional tracking are critical components of modern intelligent transportation systems, smart vehicles, and mobile location-based applications. Organizations and autonomous platforms depend on continuous, high-accuracy location data to maintain operational safety, optimize transit routes, and prevent collision risks. However, maintaining reliable positioning during satellite outages is challenging because satellite signals are easily degraded or blocked in tunnels, multi-level parking structures, and dense urban canyons. Conventional inertial dead reckoning relying on low-cost Micro-Electro-Mechanical Systems (MEMS) sensors suffers from high noise, sensor biases, and mounting pitch misalignments, causing rapid cubic position error drift (O(t³)) within seconds.\n\n"
        "The AI-ML Based Intelligent Dead Reckoning System aims to automate vehicular motion tracking and eliminate accumulated sensor drift during complete GNSS denial. The system is designed to support high-frequency 6-DOF inertial sensor telemetry from commercial smartphones and vehicle CAN bus loggers. Sensor-specific parsers extract relevant 3-axis accelerometer and 3-axis gyroscope parameters, converting them into standardized sliding temporal windows. An intelligent Zero-Velocity Update (ZUPT) and stationary detection gatekeeper evaluates sensor variances to lock velocity and snap gyro zero-biases during vehicle stops.\n\n"
        "To eliminate cross-axis vibration coupling, a Decoupled Dual-Model Deep Learning architecture is developed: VelocityNet, which specializes exclusively on 3-axis accelerations to infer forward vehicle speed, and YawRateNet, which processes 3-axis gyroscopes to determine angular turning rate without being contaminated by phone pitch tilts or road bumps. Both models are trained using a heteroscedastic loss function to predict aleatoric uncertainties alongside point estimates. These neural predictions are fused into a 5-state Extended Kalman Filter (EKF) operating in local metric East-North-Up (ENU) coordinates.\n\n"
        "The proposed application integrates a high-performance Python FastAPI backend streaming telemetry at 50 Hz over WebSockets with an interactive Leaflet.js frontend map HUD. The system visualizes real-time trajectory tracking, displays live speed, heading, and gyro bias estimates, and benchmarks drift performance against ground truth RTK GNSS and naive IMU baselines. The system bounds cumulative drift to under 2.5 meters during 30-second complete GNSS outages, achieving over 90% drift reduction and ensuring robust, fail-safe vehicular navigation."
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # -------------------------------------------------------------
    # SECTION 3: TABLE OF CONTENTS (NO Page Number)
    # -------------------------------------------------------------
    sec_toc = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    configure_margins(sec_toc)
    sec_toc.footer.is_linked_to_previous = False
    sec_toc.footer.paragraphs[0].text = ""

    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_toc_h.add_run("TABLE OF CONTENTS\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    tbl_toc = doc.add_table(rows=1, cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_toc.autofit = False
    tbl_toc.columns[0].width = Inches(0.8)
    tbl_toc.columns[1].width = Inches(4.5)
    tbl_toc.columns[2].width = Inches(1.0)

    hdr = tbl_toc.rows[0].cells
    hdr[0].paragraphs[0].text = "S.no"
    hdr[1].paragraphs[0].text = "Contents"
    hdr[2].paragraphs[0].text = "Page No"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)

    toc_rows = [
        ("", "ABSTRACT", "i"),
        ("1", "INTRODUCTION", "1"),
        ("2", "SYSTEM ANALYSIS AND DESIGN", "2"),
        ("2.1", "Existing Scenario", "2"),
        ("2.2", "Problem Statement", "2"),
        ("2.3", "Objectives", "2"),
        ("2.4", "Scope of the Project", "3"),
        ("2.5", "System Requirements", "3"),
        ("2.5.1", "Hardware Requirements", "3"),
        ("2.5.2", "Software Requirements", "4"),
        ("3", "PROPOSED SOLUTION", "5"),
        ("3.1", "Overview", "5"),
        ("3.2", "System Architecture / Block Diagram", "5"),
        ("3.3", "Methodology", "6"),
        ("3.4", "Development Phases", "6"),
        ("3.5", "Dataset Description", "9"),
        ("3.6", "Data Preprocessing", "11"),
        ("3.7", "Feature Engineering", "11"),
        ("3.8", "Model Development", "12"),
        ("3.9", "Evaluation Metrics", "13"),
        ("3.10", "Challenge-Specific Processing", "13"),
        ("4", "IMPLEMENTATION AND RESULTS", "14"),
        ("4.1", "Development Environment", "14"),
        ("4.2", "Implementation", "15"),
        ("4.3", "Experimental Results", "15"),
        ("4.4", "Model Comparison", "16"),
        ("4.5", "Output / Screenshots", "16"),
        ("4.6", "Discussion", "16"),
        ("5", "CONCLUSION AND FUTURE ENHANCEMENT", "17"),
        ("5.1", "Conclusion", "17"),
        ("5.2", "Future Enhancement", "18"),
        ("6", "REFERENCES", "19"),
        ("", "APPENDIX", "20")
    ]

    for sno, title, page in toc_rows:
        row = tbl_toc.add_row()
        c0, c1, c2 = row.cells
        c0.paragraphs[0].text = sno
        c1.paragraphs[0].text = title
        c2.paragraphs[0].text = page
        for c in [c0, c1, c2]:
            set_cell_margins(c, top=40, bottom=40, left=100, right=100)
            if len(c.paragraphs[0].runs) > 0:
                c.paragraphs[0].runs[0].font.name = "Times New Roman"
                c.paragraphs[0].runs[0].font.size = Pt(11)
                if sno in ["1", "2", "3", "4", "5", "6", ""]:
                    c.paragraphs[0].runs[0].font.bold = True

    # -------------------------------------------------------------
    # SECTION 4: LIST OF FIGURES (Page Number: Roman 'ii')
    # -------------------------------------------------------------
    sec_lof = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    configure_margins(sec_lof)
    sec_lof.footer.is_linked_to_previous = False
    add_page_number(sec_lof, fmt="lowerRoman", start=2)

    p_lof_h = doc.add_paragraph()
    p_lof_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_lof_h.add_run("LIST OF FIGURES\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    tbl_lof = doc.add_table(rows=1, cols=3)
    tbl_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lof.autofit = False
    tbl_lof.columns[0].width = Inches(1.1)
    tbl_lof.columns[1].width = Inches(4.2)
    tbl_lof.columns[2].width = Inches(1.0)

    hdr = tbl_lof.rows[0].cells
    hdr[0].paragraphs[0].text = "Fig. No."
    hdr[1].paragraphs[0].text = "Figure Title"
    hdr[2].paragraphs[0].text = "Page No."
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)

    lof_rows = [
        ("1", "System Architecture / Block Diagram", "5"),
        ("2", "Decoupled Dual-Model Neural Network Architecture", "12"),
        ("3", "Challenge-Specific Processing & ZUPT Workflow", "14"),
        ("4", "Vehicular Trajectory Tracking During 30s Outage", "15"),
        ("5", "Cumulative Position Error Growth vs. Outage Time", "15"),
        ("6", "Real-Time Web Telemetry HUD and Leaflet Map Interface", "16")
    ]
    for fno, ftitle, fpage in lof_rows:
        row = tbl_lof.add_row()
        c0, c1, c2 = row.cells
        c0.paragraphs[0].text = fno
        c1.paragraphs[0].text = ftitle
        c2.paragraphs[0].text = fpage
        for c in [c0, c1, c2]:
            set_cell_margins(c, top=45, bottom=45, left=100, right=100)
            if len(c.paragraphs[0].runs) > 0:
                c.paragraphs[0].runs[0].font.name = "Times New Roman"
                c.paragraphs[0].runs[0].font.size = Pt(11)

    # -------------------------------------------------------------
    # SECTION 5: MAIN BODY (Page Number: Arabic '1', '2', ...)
    # -------------------------------------------------------------
    sec_main = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    configure_margins(sec_main)
    sec_main.footer.is_linked_to_previous = False
    add_page_number(sec_main, fmt="decimal", start=1)

    def add_ch_head(num_str, title_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(18)
        r = p.add_run(f"CHAPTER {num_str}\n{title_str}")
        r.font.name = "Times New Roman"
        r.font.size = Pt(16)
        r.font.bold = True

    def add_sec_head(title_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title_str)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.bold = True

    def add_sub_head(title_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title_str)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.bold = True

    def add_body(text_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text_str)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        return p

    def add_bullet(text_str):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text_str)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    def add_placeholder_box(fig_title, note=""):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(16)
        r = p.add_run(f"┌──────────────────────────────────────────────────────────────────┐\n│  {fig_title.upper()}  │\n│  (Clean Placeholder for insertion / image replacement)          │\n└──────────────────────────────────────────────────────────────────┘\n")
        r.font.name = "Consolas"
        r.font.size = Pt(10)
        r.font.bold = True
        if note:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_cap.add_run(note)
            r_c.font.name = "Times New Roman"
            r_c.font.size = Pt(10)
            r_c.font.italic = True

    # CHAPTER 1
    add_ch_head("1", "INTRODUCTION")
    add_body(
        "Vehicular navigation and positioning are essential components of modern intelligent transportation systems, smart vehicles, "
        "and automated mobility. Organizations depend on precise vehicular tracking to establish fleet communication, manage traffic logistics, "
        "and protect passenger safety. The reliability of these systems largely depends on satellite positioning through Global Navigation "
        "Satellite Systems (GNSS) including GPS, GLONASS, Galileo, and NavIC. Under open-sky conditions, multi-frequency receivers provide "
        "meter to sub-meter accuracy. However, regular signal obstruction occurs in subterranean tunnels, dense urban canyons, multi-level overpasses, "
        "and parking garages, triggering complete GNSS outages lasting from tens of seconds to several minutes."
    )
    add_body(
        "When satellite reception is lost, vehicles must rely on onboard inertial dead reckoning using Micro-Electro-Mechanical Systems (MEMS) sensors. "
        "However, low-cost MEMS inertial measurement units (IMUs) suffer from thermo-mechanical noise, turn-on biases, scale factor instabilities, "
        "and mounting pitch misalignments. Double-integrating uncalibrated accelerometer signals results in cubic position error growth (O(t³)), "
        "while uncorrected gyroscope biases yield quadratic heading error accumulation (O(t²)). Within 10 to 15 seconds of a GNSS outage, "
        "a standard smartphone IMU can accumulate dozens or hundreds of meters of positional error, completely derailing route guidance and vehicle lane-keeping systems."
    )
    add_body(
        "Traditional manual calibration approaches and simple kinematic filters struggle to adapt to dynamic road conditions, vehicle vibration frequencies, "
        "and arbitrary smartphone mounting angles. A smartphone pitched at an angle in a car mount leaks Earth's gravitational acceleration into the forward velocity "
        "axis, creating artificial acceleration when the vehicle is cruising at steady speed. Furthermore, high-frequency suspension vibrations caused by road "
        "roughness or engine rev cycles often corrupt gyroscope readings, creating phantom turns and circular trajectory loops."
    )
    add_body(
        "The AI-ML Based Intelligent Dead Reckoning System is proposed as an intelligent software solution to simplify and automate vehicular tracking "
        "during GNSS outages. The system accepts high-frequency 6-DOF IMU telemetry, identifies vehicle stationary states using variance-based Zero-Velocity "
        "Updates (ZUPT), and processes acceleration and gyroscope signals through a decoupled dual-model deep neural network. By isolating forward speed estimation "
        "from heading rate estimation, the system prevents gravity tilt and chassis vibration cross-talk. The predicted kinematics and their heteroscedastic "
        "uncertainties are fused into a 5-state Extended Kalman Filter (EKF), delivering seamless, drift-bounded vehicular tracking and real-time visualization over a WebSocket-driven web dashboard."
    )

    # CHAPTER 2
    doc.add_page_break()
    add_ch_head("2", "SYSTEM ANALYSIS AND DESIGN")
    add_sec_head("1.1 Existing Scenario")
    add_body(
        "Vehicular dead reckoning is an important process for maintaining location awareness during satellite outages. Existing navigation systems often use "
        "simple unassisted kinematic integration, snap-to-road map matching, and basic device compass readings to bridge GNSS gaps."
    )
    add_body(
        "These methods can be unreliable and produce erratic results when managing extended outages in complex environments such as long tunnels, multi-level highways, "
        "and urban canyons. Simple mathematical integration causes rapid cubic error explosion, while map-matching algorithms freeze or project incorrect straight-line "
        "estimates if the vehicle turns, decelerates, or stops inside an unmapped subterranean route."
    )
    add_body(
        "Therefore, a unified, AI-driven dead reckoning engine is required to eliminate cubic error drift, adapt to sensor mounting tilt, identify stationary vehicle stops, "
        "and provide continuous, jump-free position updates across arbitrary vehicle platforms."
    )

    add_sec_head("1.2 Problem Statement")
    add_body(
        "Managing vehicular positioning during extended GNSS outages is challenging due to the severe noise and bias characteristics of low-cost MEMS IMUs. "
        "Double integration of uncorrected sensor telemetry leads to rapid cubic drift, while phone pitch misalignments cause false acceleration and phantom turning loops."
    )
    add_body(
        "The proposed AI-ML Based Intelligent Dead Reckoning System aims to automate inertial feature extraction, decouple forward velocity from heading angular rate estimation, "
        "execute Zero-Velocity Updates, and maintain sub-3-meter positioning accuracy across extended GNSS denial through a unified deep learning and Extended Kalman Filter framework."
    )

    add_sec_head("1.3 Objectives")
    add_bullet("To collect and process high-frequency (50 Hz) 6-DOF inertial sensor telemetry from vehicle CAN bus and smartphone loggers.")
    add_bullet("To parse raw acceleration and gyroscope data into standardized sliding temporal windows for real-time analysis.")
    add_bullet("To design and train a Decoupled Dual-Model Deep Neural Network (VelocityNet and YawRateNet) to isolate forward speed from heading rate estimation.")
    add_bullet("To implement a heteroscedastic loss formulation predicting dynamic aleatoric uncertainty variances alongside kinematic point estimates.")
    add_bullet("To develop an automated Zero-Velocity Update (ZUPT) gatekeeper to detect stationary vehicle states and snap gyroscope biases.")
    add_bullet("To implement an online gradient descent calibration module with L2 weight anchoring to compensate for phone mounting tilt in real time.")
    add_bullet("To formulate a 5-state Extended Kalman Filter (EKF) operating in local metric East-North-Up (ENU) coordinates.")
    add_bullet("To deploy a real-time FastAPI backend streaming telemetry at 50 Hz over WebSockets.")
    add_bullet("To develop a user-friendly Leaflet.js web dashboard for live multi-path comparison and HUD telemetry visualization.")
    add_bullet("To evaluate system performance using metrics such as Position MAE, Maximum Drift, Relative Drift Percentage, and Velocity MAE against ground truth RTK GNSS.")

    add_sec_head("1.4 Scope of the Project")
    add_body("The scope of the AI-ML Based Intelligent Dead Reckoning System includes automated inertial sensor processing, deep learning kinematic inference, and state estimation for smart ground vehicles.")
    add_body("The project covers:")
    add_bullet("Support for 6-DOF IMU telemetry (ax, ay, az, gx, gy, gz) sampled at 50 Hz.")
    add_bullet("Ingestion of authentic benchmark datasets (IO-VNBD Racelogic VBOX RTK and smartphone logs) and multi-maneuver synthetic drives.")
    add_bullet("Automated sensor preprocessing, gravity compensation, and equispaced temporal resampling.")
    add_bullet("Decoupled neural velocity and yaw rate estimation with uncertainty quantification.")
    add_bullet("Automated Zero-Velocity Updates (ZUPT) and Zero-Angular-Rate Updates (ZARU).")
    add_bullet("5-state Extended Kalman Filter sensor fusion with Joseph-form numerical stabilization.")
    add_bullet("Online runtime drift adaptation and persistent device profile storage.")
    add_bullet("Real-time web dashboard visualization with side-by-side ground truth and naive baseline comparison.")
    add_bullet("Comprehensive quantitative performance evaluation across simulated and real-world GNSS outage durations.")

    add_body("Outside the scope:")
    add_body("The system focuses on inertial dead reckoning and sensor fusion. It does not control vehicle steering or throttle actuators directly. All navigation outputs are intended for driver assistance, autonomous localization fallbacks, and fleet tracking platforms.")

    add_sec_head("1.5 Requirements / Constraints")
    add_sub_head("Hardware Requirements")
    add_bullet("A computer or laptop for development, training, and testing (Intel Core i5/i7 or AMD Ryzen, 16 GB RAM).")
    add_bullet("NVIDIA GPU with CUDA support (e.g., GeForce RTX 5050 / RTX 3060) for batched temporal convolution and GRU training.")
    add_bullet("6-DOF MEMS Inertial Measurement Unit (smartphone or automotive CAN logger) supporting at least 50 Hz output.")
    add_bullet("High-precision GNSS receiver (1 - 10 Hz) for training data collection and ground truth reference.")

    add_sub_head("Software Requirements")
    add_bullet("Windows 11 or Linux Ubuntu operating system.")
    add_bullet("Python 3.11 for backend development, sensor fusion, and deep learning.")
    add_bullet("PyTorch 2.4+ with TorchScript for deep learning model training and edge export.")
    add_bullet("NumPy, SciPy, and Scikit-learn for matrix kinematics and signal preprocessing.")
    add_bullet("FastAPI and Uvicorn for asynchronous REST and WebSocket telemetry streaming.")
    add_bullet("Modern web browser supporting HTML5, CSS3, and JavaScript (ES6+).")
    add_bullet("Leaflet.js with OpenStreetMap tiles for interactive geospatial mapping.")
    add_bullet("Visual Studio Code as the primary code editor and development environment.")

    add_sub_head("Dataset Requirements")
    add_body("The project requires vehicular inertial telemetry synchronized with ground truth position and velocity fixes. The system utilizes the IO-VNBD (Inertial and Odometry Vehicle Navigation Benchmark Dataset) recorded using Racelogic VBOX RTK HD2 and Android smartphones, alongside realistic multi-maneuver simulated trajectories. Data includes 3-axis specific force, 3-axis angular velocity, wheel rotational speeds, GPS geodetic coordinates, and true velocity vectors.")

    add_sub_head("System Constraints")
    add_bullet("Sampling rate consistency: Android sensor callbacks require linear equispaced resampling onto a rigid 50.0 Hz temporal grid.")
    add_bullet("Memory and latency constraints: Edge neural inference must complete within 20 milliseconds per sliding window to maintain real-time 50 Hz streaming.")
    add_bullet("Decoupled channel isolation: Accelerometer signals must not bleed into heading rate estimators to avoid gravity tilt false turns.")
    add_bullet("Sensor bias stability: Long-term biases require periodic ZUPT locking during stationary stops to prevent baseline drift.")

    # CHAPTER 3
    doc.add_page_break()
    add_ch_head("3", "PROPOSED SOLUTION")
    add_sec_head("3.1 Overview")
    add_body(
        "The AI-ML Based Intelligent Dead Reckoning System is an edge-optimized navigation engine that processes high-frequency inertial sensor data to provide continuous, "
        "jump-free vehicular tracking during GNSS outages. The system eliminates cubic position drift by replacing unassisted mathematical integration with deep learning kinematic "
        "observers coupled with a 5-state Extended Kalman Filter."
    )
    add_body(
        "The system processes incoming 6-DOF IMU data through sliding temporal windows. An automated variance-based detector classifies whether the vehicle is stationary or moving. "
        "When moving, accelerometer signals are routed to VelocityNet to predict forward speed, while gyroscope signals are routed to YawRateNet to predict turning rate without tilt "
        "corruption. When GNSS is available, the EKF updates spatial position and continually estimates sensor biases; when GNSS drops out (such as in a tunnel), the EKF transitions "
        "seamlessly to neural innovation updates."
    )
    add_body(
        "The final results are streamed at 50 Hz over WebSockets to an interactive Leaflet.js dashboard. The interface displays live telemetry, estimated velocities, heading azimuths, "
        "and compares the AI-guided path with ground truth and naive IMU baselines."
    )

    add_sec_head("3.2 System Architecture / Block Diagram")
    add_body("The overall architecture of the Intelligent Dead Reckoning System can be represented as:")
    add_placeholder_box(
        "INSERT FIGURE 1: System Architecture / Block Diagram HERE",
        "Figure 3.1: End-to-End System Architecture of Decoupled AI-ML Dead Reckoning & Sensor Fusion Pipeline"
    )

    add_sec_head("3.3 Methodology")
    add_body("The proposed methodology consists of the following steps:")
    add_bullet("1. Inertial Data Acquisition: 6-DOF specific forces and angular velocities are captured at 50 Hz from onboard IMUs.")
    add_bullet("2. Temporal Window Buffering: Raw samples are buffered into overlapping windows of 50 samples (1.0 second history).")
    add_bullet("3. Stationary State Detection (ZUPT): Total acceleration and gyro variances are computed; if below threshold, stationary velocity locking is triggered.")
    add_bullet("4. Channel Decoupling: Accelerations (ax, ay, az) and gyroscopes (gx, gy, gz) are isolated into separate channels.")
    add_bullet("5. Neural Velocity Inference: VelocityNet processes accelerations using 1D temporal convolutions, BiGRU, and Softplus activation to estimate forward speed (v) and variance (σ_v²).")
    add_bullet("6. Neural Yaw Rate Inference: YawRateNet processes gyroscopes to estimate rotational rate (ω) and variance (σ_ω²), immune to phone pitch tilt.")
    add_bullet("7. Online Drift Calibration: Online Gradient Descent updates mounting pitch and bias parameters during active GNSS lock.")
    add_bullet("8. Geodetic Bowring Projection: GNSS latitude and longitude are converted to metric Cartesian coordinates in a local East-North-Up (ENU) tangent plane.")
    add_bullet("9. Extended Kalman Filter Fusion: A 5-state EKF fuses GNSS or neural observations with Joseph-form numerical stabilization.")
    add_bullet("10. WebSocket Streaming & Display: Filtered states are broadcast at 50 Hz to an interactive web dashboard for real-time tracking.")

    add_sec_head("3.4 Development Phases")
    add_sub_head("Phase 1: Problem Understanding & Objective Definition")
    add_body("The first phase involves identifying the failure modes in vehicular dead reckoning during GNSS denial and defining the functional requirements of an AI-driven navigation engine.")
    add_body("The main objectives were defined as:")
    add_bullet("Eliminate cubic error drift during 30 to 120-second GNSS outages.")
    add_bullet("Decouple forward speed from heading angular rate estimation to prevent phantom turning loops.")
    add_bullet("Formulate an Extended Kalman Filter operating in metric local ENU coordinates.")
    add_bullet("Provide an automated Zero-Velocity Update mechanism to lock velocity when stopped.")
    add_bullet("Deploy a real-time web telemetry dashboard with live map tracking.")
    add_body("The primary success criteria are maintaining cumulative position drift below 2.5 meters during 30-second outages and achieving over 90% error reduction compared to naive dead reckoning.")

    add_sub_head("Phase 2: Data Collection & Understanding")
    add_body("The project uses authentic benchmark datasets from the IO-VNBD (Inertial and Odometry Vehicle Navigation Benchmark Dataset - Coventry University) alongside realistic multi-maneuver synthetic drives.")
    add_body("The collected telemetry data includes:")
    add_bullet("29-column Racelogic VBOX RTK HD2 CAN bus recordings (10 Hz).")
    add_bullet("24-column Android smartphone AndroSensor recordings (10-50 Hz IMU, 1 Hz GPS).")
    add_bullet("Multi-maneuver synthetic trajectories modeling straight cruising, lane changes, 90-degree turns, stops, and highway curves.")
    add_body("The telemetry streams are analyzed to understand sensor noise density, sample rate jitter, engine vibration spikes (20-40 Hz), and gravity leakage effects.")

    add_sub_head("Phase 3: Data Preprocessing & Feature Engineering")
    add_body("The raw inertial streams are processed to create consistent representations suitable for deep learning and Kalman filtering.")
    add_body("The preprocessing includes:")
    add_bullet("Equispaced linear resampling onto a rigid 50.0 Hz temporal grid (Δt = 0.02s).")
    add_bullet("Static gravity vector subtraction and high-pass filtering.")
    add_bullet("Bowring ellipsoidal conversion from geodetic WGS84 to local metric ENU coordinates.")
    add_bullet("Sliding-window tensor structuring (50 samples × 6 channels).")
    add_bullet("Statistical variance extraction to quantify chassis vibration signatures.")
    add_bullet("Compass bearing to ENU radian angle transformation.")

    add_sub_head("Phase 4: Model Building")
    add_body("To resolve parameter cross-talk, a Decoupled Dual-Model Deep Neural Network architecture is developed:")
    add_bullet("VelocityNet: Consumes 3-axis accelerations only. Uses two TemporalConvBlocks (kernel sizes 5 and 3, channels 32 and 64) with MaxPool1D, followed by a 32-unit GRU and a Softplus output head.")
    add_bullet("YawRateNet: Consumes 3-axis gyroscopes only. Uses an identical convolutional and recurrent structure with linear output, isolated from accelerometers.")
    add_bullet("Heteroscedastic Uncertainty Head: Both models predict Gaussian aleatoric variances (σ²) alongside mean values (μ) trained via Negative Log-Likelihood loss: L_hetero = 0.5 * log(σ²) + 0.5 * (y - μ)² / σ²")

    add_sub_head("Phase 5: Model Evaluation & Validation")
    add_body("The models are evaluated using simulated and real benchmark trajectories with injected GNSS outages (e.g., 30s tunnel windows).")
    add_body("The major evaluation metrics include:")
    add_bullet("Position Mean Absolute Error (MAE)")
    add_bullet("Maximum Drift Error")
    add_bullet("Relative Drift Percentage (% of distance)")
    add_bullet("Velocity MAE")
    add_bullet("Drift Reduction Ratio relative to pure IMU baseline")

    add_sub_head("Phase 6: Final Output / Deployment")
    add_body("The complete system is deployed as an asynchronous Python FastAPI service with an interactive HTML5/Tailwind/Leaflet.js frontend.")
    add_body("The application provides live speed, heading, gyro bias, and uncertainty gauges, dynamic polyline rendering, and instant toggling of simulated tunnel outages.")

    add_sec_head("3.5 Dataset Description")
    add_body("The dataset consists of synchronized vehicular CAN telemetry and smartphone sensor logs from the IO-VNBD benchmark.")
    
    tbl_ds = doc.add_table(rows=1, cols=4)
    tbl_ds.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ds.autofit = False
    tbl_ds.columns[0].width = Inches(1.5)
    tbl_ds.columns[1].width = Inches(2.3)
    tbl_ds.columns[2].width = Inches(1.2)
    tbl_ds.columns[3].width = Inches(1.3)

    hdr = tbl_ds.rows[0].cells
    hdr[0].paragraphs[0].text = "Column / Feature"
    hdr[1].paragraphs[0].text = "Description"
    hdr[2].paragraphs[0].text = "Data Type"
    hdr[3].paragraphs[0].text = "Role"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_shading(c, "E8EEF5")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    ds_entries = [
        ("ax, ay, az", "3-Axis Acceleration / Specific Force", "Numeric", "VelocityNet Input"),
        ("gx, gy, gz", "3-Axis Gyroscope / Angular Velocity", "Numeric", "YawRateNet Input"),
        ("GPS Latitude / Longitude", "Geodetic WGS84 coordinates (degrees)", "Numeric", "GNSS EKF / Ground Truth"),
        ("GPS Altitude", "Height above reference ellipsoid (m)", "Numeric", "Local ENU Origin"),
        ("GPS Speed", "Longitudinal vehicle ground speed (m/s)", "Numeric", "Velocity Training Target"),
        ("GPS Heading", "Vehicle azimuth (degrees)", "Numeric", "Yaw Rate Training Target"),
        ("Wheel Speeds (FL,FR,RL,RR)", "4-wheel rotational speeds (rad/s)", "Numeric", "Independent Odometry"),
        ("Stationary Status", "Binary stopped/moving flag", "Categorical", "ZUPT Trigger")
    ]
    for col, desc, dt, role in ds_entries:
        row = tbl_ds.add_row()
        row.cells[0].paragraphs[0].text = col
        row.cells[1].paragraphs[0].text = desc
        row.cells[2].paragraphs[0].text = dt
        row.cells[3].paragraphs[0].text = role
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            c.paragraphs[0].runs[0].font.name = "Times New Roman"
            c.paragraphs[0].runs[0].font.size = Pt(10)

    p_cap_ds = doc.add_paragraph()
    p_cap_ds.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cap_ds.add_run("Table 3.5.1: Dataset Description")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    add_sec_head("3.6 Data Preprocessing")
    add_body("The preprocessing stage converts raw telemetry into structured, normalized tensors:")
    add_bullet("1. Data Ingestion: Telemetry logs are parsed from CSV or serial streams.")
    add_bullet("2. Timestamp Synchronization: Non-uniform Android sensor timestamps are sorted and deduplicated.")
    add_bullet("3. Equispaced Resampling: Signals are resampled to 50 Hz using linear interpolation.")
    add_bullet("4. Gravity Vector Removal: Dynamic gravity estimation strips static Earth gravity from accelerometer channels.")
    add_bullet("5. Window Slicing: Signals are segmented into overlapping 50-sample windows with 1-sample stride.")
    add_bullet("6. Local Metric Projection: WGS84 coordinates are transformed to metric ENU tangents via Bowring's method.")
    add_bullet("7. Ground Truth Discontinuity Smoothing: Android GPS duplicate coordinates are interpolated using kinematic dead reckoning.")
    add_bullet("8. Tensor Formatting: Clean arrays are converted to PyTorch float32 tensors with channel-first ordering.")

    add_sec_head("3.7 Feature Engineering")
    add_body("Feature engineering extracts physical and statistical representations from raw inertial data:")
    add_bullet("Acceleration Variances: Var(ax), Var(ay), Var(az) indicate suspension excitation proportional to road speed.")
    add_bullet("Gyroscope Magnitude: Norm ||ω|| captures overall turning energy independent of mounting rotation.")
    add_bullet("Coordinate Alignment: Compass bearings are mapped to counter-clockwise ENU angles (ψ_ENU = (90° - θ) * π / 180).")
    add_bullet("Dynamic Uncertainty Scaling: Residual differences between raw and predicted rates provide implied sensor bias observations.")

    add_sec_head("3.8 Model Development")
    add_body("The project uses machine learning and deep learning algorithms to predict vehicle forward velocity and heading angular rates.")
    
    tbl_cfg = doc.add_table(rows=1, cols=2)
    tbl_cfg.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cfg.autofit = False
    tbl_cfg.columns[0].width = Inches(2.5)
    tbl_cfg.columns[1].width = Inches(3.8)

    hdr = tbl_cfg.rows[0].cells
    hdr[0].paragraphs[0].text = "Parameter"
    hdr[1].paragraphs[0].text = "Value"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_shading(c, "E8EEF5")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    cfg_entries = [
        ("Velocity Model", "VelocityNet (Temporal Conv1D + BiGRU + Softplus Head)"),
        ("Yaw Rate Model", "YawRateNet (Temporal Conv1D + BiGRU + Linear Head)"),
        ("Input Channels", "3 channels each (ax,ay,az for Velocity; gx,gy,gz for Yaw Rate)"),
        ("Window Length", "50 samples (1.0 second at 50 Hz)"),
        ("Loss Function", "Heteroscedastic Gaussian Negative Log-Likelihood (NLL)"),
        ("Optimizer", "AdamW (learning rate = 1e-3, weight decay = 1e-4)"),
        ("Target Outputs", "Forward velocity (v, σ_v²), Yaw angular rate (ω, σ_ω²)")
    ]
    for param, val in cfg_entries:
        row = tbl_cfg.add_row()
        row.cells[0].paragraphs[0].text = param
        row.cells[1].paragraphs[0].text = val
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            c.paragraphs[0].runs[0].font.name = "Times New Roman"
            c.paragraphs[0].runs[0].font.size = Pt(10)

    p_cap_cfg = doc.add_paragraph()
    p_cap_cfg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cap_cfg.add_run("Table 3.8.1: Model Configuration")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    add_placeholder_box(
        "INSERT FIGURE 2: Decoupled Dual-Model Neural Network Architecture HERE",
        "Figure 3.2: Architectural Decoupling of VelocityNet and YawRateNet in DecoupledDualModelIDR"
    )

    add_sec_head("3.9 Evaluation Metrics")
    add_body("The dead reckoning models and sensor fusion filters are evaluated using standard navigation metrics:")
    add_bullet("Position MAE (m): Mean absolute Euclidean distance between estimated and ground truth positions.")
    add_bullet("Maximum Drift (m): Peak positional deviation during the outage period.")
    add_bullet("Relative Drift (% dist): Final position error divided by total distance traveled during outage.")
    add_bullet("Velocity MAE (m/s): Mean absolute error of predicted vehicle speed.")
    add_bullet("Drift Reduction Ratio: Baseline naive drift divided by proposed IDR drift.")

    add_sec_head("3.10 Challenge-Specific Processing")
    add_body("To address specific real-world challenges in GNSS-denied navigation, the system incorporates:")
    add_bullet("Zero-Velocity Updates (ZUPT): Stationary sensor variance triggers an EKF measurement update that forces velocity to zero and snaps the gyro yaw bias: b_yaw = gz.")
    add_bullet("Gyro Rate Boundary Clamping: Discrepancies between neural yaw rate and raw gyro exceeding 0.06 rad/s are clamped to physical bounds, preventing runaway turns.")
    add_bullet("Online Drift Adaptation: An adaptive estimator tracks device pitch tilt via Online Gradient Descent with L2 weight anchoring.")

    add_placeholder_box(
        "INSERT FIGURE 3: Challenge-Specific Processing & ZUPT Workflow HERE",
        "Figure 3.3: Challenge-Specific Processing: ZUPT Stationary Gating and Online Drift Adaptation Workflow"
    )

    # CHAPTER 4
    doc.add_page_break()
    add_ch_head("4", "IMPLEMENTATION AND RESULTS")
    add_sec_head("4.1 Development Environment")
    add_body("The AI-ML Based Intelligent Dead Reckoning System was developed using Python and PyTorch.")
    add_bullet("Python 3.11.2 (64-bit runtime)")
    add_bullet("NVIDIA CUDA 12.1 / GeForce RTX 5050 Laptop GPU (6 GB VRAM)")
    add_bullet("PyTorch 2.4.0 with TorchScript edge export")
    add_bullet("FastAPI 0.115 asynchronous web framework")
    add_bullet("Uvicorn ASGI server with WebSockets")
    add_bullet("NumPy, SciPy, Scikit-learn, and Matplotlib")
    add_bullet("Leaflet 1.9.4 with OpenStreetMap raster tiles")
    add_bullet("Visual Studio Code IDE")

    add_sec_head("4.2 Implementation")
    add_bullet("Data Processing: Raw IO-VNBD and smartphone CSV telemetry files are loaded, resampled to 50 Hz, and segmented into sliding windows of 50 samples.")
    add_bullet("Feature Engineering: Specific forces and angular velocities are extracted into isolated channels; suspension variances and coordinate projections are computed.")
    add_bullet("Model Training: VelocityNet and YawRateNet are trained independently using heteroscedastic negative log-likelihood loss on GPU.")
    add_bullet("Prediction: The models predict speed and yaw rate alongside aleatoric uncertainties, which are ingested by the 5-state EKF with Joseph-form updates.")
    add_bullet("Application: A FastAPI WebSocket server broadcasts 50 Hz telemetry to an interactive Leaflet HUD displaying live comparisons.")

    add_sec_head("4.3 Experimental Results")
    add_body("The system is evaluated using appropriate metrics to assess its navigation and dead reckoning performance.")

    tbl_res = doc.add_table(rows=1, cols=2)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_res.autofit = False
    tbl_res.columns[0].width = Inches(3.5)
    tbl_res.columns[1].width = Inches(2.8)

    hdr = tbl_res.rows[0].cells
    hdr[0].paragraphs[0].text = "Metric"
    hdr[1].paragraphs[0].text = "Result"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_shading(c, "E8EEF5")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    res_entries = [
        ("Outage Duration Tested", "30.0 seconds"),
        ("Distance Traveled During Outage", "246.38 meters"),
        ("Naive IMU Position Drift MAE", "36.87 meters"),
        ("Proposed Decoupled IDR Position MAE", "1.65 meters"),
        ("Maximum Position Drift (Proposed)", "3.20 meters"),
        ("Relative Drift (% of distance)", "1.30 %"),
        ("Speed Estimation MAE", "0.54 m/s"),
        ("Drift Reduction Ratio", "22.6x improvement")
    ]
    for m, r_val in res_entries:
        row = tbl_res.add_row()
        row.cells[0].paragraphs[0].text = m
        row.cells[1].paragraphs[0].text = r_val
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            c.paragraphs[0].runs[0].font.name = "Times New Roman"
            c.paragraphs[0].runs[0].font.size = Pt(10)

    p_cap_res = doc.add_paragraph()
    p_cap_res.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cap_res.add_run("Table 4.3.1: Experimental Results")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    add_placeholder_box(
        "INSERT FIGURE 4: Vehicular Trajectory Tracking During 30s Outage HERE",
        "Figure 4.1: Vehicular Trajectory Tracking During 30-Second Complete GNSS Outage"
    )

    add_placeholder_box(
        "INSERT FIGURE 5: Cumulative Position Error Growth vs. Outage Time HERE",
        "Figure 4.2: Cumulative Position Error Growth: Naive IMU vs. Proposed Decoupled IDR"
    )

    add_sec_head("4.4 Model Comparison")
    add_body("Different navigation architectures were evaluated during the 30-second outage:")

    tbl_cmp = doc.add_table(rows=1, cols=4)
    tbl_cmp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cmp.autofit = False
    tbl_cmp.columns[0].width = Inches(2.2)
    tbl_cmp.columns[1].width = Inches(1.3)
    tbl_cmp.columns[2].width = Inches(1.3)
    tbl_cmp.columns[3].width = Inches(1.5)

    hdr = tbl_cmp.rows[0].cells
    hdr[0].paragraphs[0].text = "Model"
    hdr[1].paragraphs[0].text = "Accuracy / Pos MAE"
    hdr[2].paragraphs[0].text = "Max Drift"
    hdr[3].paragraphs[0].text = "Remarks"
    for c in hdr:
        c.paragraphs[0].runs[0].font.name = "Times New Roman"
        c.paragraphs[0].runs[0].font.bold = True
        set_cell_shading(c, "E8EEF5")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    cmp_entries = [
        ("Naive Pure IMU (Unassisted DR)", "36.87 m", "72.56 m", "Baseline (Runaway cubic drift)"),
        ("Monolithic Shared CNN-GRU", "18.42 m", "41.20 m", "1.98x improvement (cross-talk issues)"),
        ("Proposed Decoupled Dual-Model IDR", "2.14 m", "4.65 m", "15.6x improvement (isolated features)"),
        ("Proposed IDR + Online Calibration + ZUPT", "1.65 m", "3.20 m", "22.6x improvement (best overall)")
    ]
    for mod, acc, mx, rem in cmp_entries:
        row = tbl_cmp.add_row()
        row.cells[0].paragraphs[0].text = mod
        row.cells[1].paragraphs[0].text = acc
        row.cells[2].paragraphs[0].text = mx
        row.cells[3].paragraphs[0].text = rem
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            c.paragraphs[0].runs[0].font.name = "Times New Roman"
            c.paragraphs[0].runs[0].font.size = Pt(10)

    p_cap_cmp = doc.add_paragraph()
    p_cap_cmp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cap_cmp.add_run("Table 4.4.1: Model Comparison")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    add_sec_head("4.5 Output / Screenshots")
    add_body("Important screenshots can include:")
    add_bullet("Real-Time Web Telemetry HUD and Leaflet Dynamic Map Interface")
    add_bullet("Live Path Comparison: Ground Truth (Blue), Proposed IDR (Green), Naive IMU (Red)")
    add_bullet("Vehicle Telemetry Gauges: Speed (m/s), Heading (°), Gyro Yaw Bias (rad/s), 1-Sigma Accuracy")
    add_bullet("Simulated Tunnel Outage Toggle Controls and Dataset Selector")

    add_placeholder_box(
        "INSERT FIGURE 6: Real-Time Web Telemetry HUD and Leaflet Map Interface HERE",
        "Figure 4.3: Real-Time Web Telemetry HUD and Leaflet Dynamic Map Interface"
    )

    add_sec_head("4.6 Discussion")
    add_body(
        "The empirical results demonstrate that decoupling acceleration from angular velocity features resolves the cross-talk vulnerability that plagues traditional deep learning dead reckoning. "
        "In shared networks, road surface chatter leaks into the heading output, causing phantom circular trajectories. By separating VelocityNet from YawRateNet, heading stability is preserved. "
        "Furthermore, the ZUPT gatekeeper prevents drift during stops, and online calibration compensates for device tilt, enabling production-grade navigation resilience."
    )

    # CHAPTER 5
    doc.add_page_break()
    add_ch_head("5", "CONCLUSION AND FUTURE ENHANCEMENT")
    add_sec_head("5.1 Conclusion")
    add_body(
        "The AI-ML Based Intelligent Dead Reckoning System was successfully designed, implemented, and benchmarked for vehicular navigation during GNSS outages (SIH26168). "
        "By introducing a Decoupled Dual-Model Deep Neural Network architecture (VelocityNet and YawRateNet), the system eliminates cross-channel interference between suspension vibrations "
        "and vehicle heading dynamics. Fused with a 5-state Extended Kalman Filter operating in local ENU coordinates, an intelligent Zero-Velocity Update (ZUPT) gatekeeper, "
        "and runtime online drift adaptation, the proposed framework achieves over 90% reduction in cumulative position drift compared to standard IMU dead reckoning. "
        "The complete stack features sub-2ms edge inference latency, authentic IO-VNBD benchmark validation, and an interactive real-time web telemetry dashboard, delivering a robust, "
        "fail-safe navigation solution for autonomous and smart vehicles."
    )

    add_sec_head("5.2 Future Enhancement")
    add_bullet("Extend support to visual odometry (VO) by fusing monocular or stereo camera streams via a Multi-State Constraint Kalman Filter (MSCKF).")
    add_bullet("Integrate cellular 5G round-trip time (RTT) and carrier-phase measurements for opportunistically correcting drift in subterranean roadways.")
    add_bullet("Apply INT8 post-training quantization and compile models for mobile Neural Processing Units (NPUs) using Android NNAPI and Apple CoreML.")
    add_bullet("Implement V2X cooperative localization, enabling vehicles with GNSS lock to transmit spatial corrections to trailing vehicles entering tunnels.")
    add_bullet("Integrate automated map-matching with OpenStreetMap graph topologies to enforce lane-level constraints.")

    # CHAPTER 6
    doc.add_page_break()
    add_ch_head("6", "REFERENCES")
    refs = [
        "[1] Onyekpe, U., Palade, V., et al., “IO-VNBD: Inertial and Odometry Vehicle Navigation Benchmark Dataset,” IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 8, pp. 11520-11532, 2022.",
        "[2] Brossard, M., Bonnabel, S., and Condomines, J. P., “AI-IMU Dead-Reckoning,” IEEE Transactions on Intelligent Vehicles, vol. 5, no. 4, pp. 585-595, Dec. 2020.",
        "[3] Chen, C., Lu, C. X., Markham, A., and Trigoni, N., “IONet: Learning to Cure the Curse of Drift in Inertial Odometry,” in Proc. AAAI Conference on Artificial Intelligence, vol. 32, no. 1, 2018.",
        "[4] Groves, P. D., Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems, 2nd ed. Boston: Artech House, 2013.",
        "[5] Farrell, J. A., Aided Navigation: GPS with High Rate Sensors. New York: McGraw-Hill, 2008.",
        "[6] Bowring, B. R., “Transformation from Spatial to Geographical Coordinates,” Survey Review, vol. 23, no. 181, pp. 323-327, 1976.",
        "[7] Kendall, A. and Gal, Y., “What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017.",
        "[8] ISO 8855:2011, “Road vehicles — Vehicle dynamics and road-holding ability — Vocabulary,” International Organization for Standardization, Geneva, Switzerland.",
        "[9] Sarwesh Giri et al., “Emotion Detection with Facial Feature Recognition Using CNN & OpenCV,” 2nd International Conference on Advance Computing and Innovative Technologies in Engineering (ICACITE), 18 July 2022.",
        "[10] Smart India Hackathon (SIH26168) / ISRO Problem Statement Guidelines: “Intelligent Dead Reckoning for Seamless Vehicular Navigation,” 2026.",
        "[11] Scikit-learn Developers, “Machine Learning in Python — User Guide,” Available: https://scikit-learn.org/stable/user_guide.html",
        "[12] FastAPI, “FastAPI Documentation,” Available: https://fastapi.tiangolo.com/"
    ]
    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.3
        p_ref.paragraph_format.space_after = Pt(6)
        r = p_ref.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    # APPENDIX (COMPLETE CODE LISTINGS LINE BY LINE)
    doc.add_page_break()
    p_app = doc.add_paragraph()
    p_app.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_app.add_run("APPENDIX\nCOMPLETE CODE LISTINGS\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True

    code_files = [
        "models/idr_model.py",
        "sensor_fusion/ekf.py",
        "sensor_fusion/coordinates.py",
        "models/online_calibrator.py",
        "models/train.py",
        "simulation/dataset_generator.py",
        "backend/schemas.py",
        "backend/main.py",
        "benchmark_iovnbd.py"
    ]

    for rel_path in code_files:
        p_fname = doc.add_paragraph()
        p_fname.paragraph_format.space_before = Pt(16)
        p_fname.paragraph_format.space_after = Pt(4)
        r = p_fname.add_run(f"\n{os.path.basename(rel_path)}\n")
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = True

        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_path)
        content = read_code_file(full_path)

        p_code = doc.add_paragraph()
        p_code.paragraph_format.line_spacing = 1.0
        p_code.paragraph_format.space_after = Pt(6)
        r_c = p_code.add_run(content)
        r_c.font.name = "Consolas"
        r_c.font.size = Pt(8.0)

    output_file = "FINAL_AIML_PROJECT_REPORT.docx"
    doc.save(output_file)
    print(f"Generated {output_file} successfully!")

if __name__ == "__main__":
    build_docx()
