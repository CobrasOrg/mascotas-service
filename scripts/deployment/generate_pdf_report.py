#!/usr/bin/env python3
"""
Script para generar reportes PDF de pruebas de despliegue.
Crea un reporte profesional con logo, tablas y estadísticas detalladas.
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

def generate_pdf_report(test_results, passed, total):
    """
    Generar reporte PDF profesional con la estructura completa.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    try:
        # Crear directorio de reports si no existe
        os.makedirs("reports", exist_ok=True)
        
        # Nombre del archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"deployment_test_report_{timestamp}.pdf"
        filepath = os.path.join("reports", filename)
        
        # Crear documento PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen
        )
        
        normal_style = styles['Normal']
        heading_style = styles['Heading3']
        
        # Título principal
        story.append(Paragraph("REPORTE DE PRUEBAS DE DESPLIEGUE", title_style))
        story.append(Spacer(1, 20))
        
        # Logo de la universidad (si existe)
        logo_path = Path("assets/university_logo.png")
        if logo_path.exists():
            try:
                img = Image(str(logo_path), width=2*inch, height=1*inch)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 20))
            except Exception as e:
                print(f"⚠️ No se pudo cargar el logo: {e}")
        
        # Información del proyecto
        story.append(Paragraph("Servicio de Mascotas - API REST", subtitle_style))
        story.append(Spacer(1, 20))
        
        # Tabla de información del proyecto
        project_info = [
            ['Campo', 'Valor'],
            ['Proyecto', 'Servicio de Mascotas - API REST'],
            ['Versión', '1.0'],
            ['Fecha de Generación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ['Entorno', 'Desarrollo Local'],
            ['Tipo de Test', 'Pruebas de Despliegue']
        ]
        
        project_table = Table(project_info, colWidths=[1.5*inch, 4*inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(project_table)
        story.append(Spacer(1, 20))
        
        # Resultado de pruebas
        story.append(Paragraph("RESULTADO DE PRUEBAS", heading_style))
        story.append(Spacer(1, 10))
        
        # Crear tabla de resultados de pruebas
        test_results_data = [['Prueba', 'Estado', 'Descripción']]
        
        for test_name, result in test_results.items():
            status = result['status']
            description = result.get('details', 'Prueba completada exitosamente')
            test_results_data.append([test_name, status, description])
        
        test_table = Table(test_results_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        test_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(test_table)
        story.append(Spacer(1, 20))
        
        # Resumen ejecutivo
        story.append(Paragraph("RESUMEN EJECUTIVO", heading_style))
        story.append(Spacer(1, 10))
        
        summary_data = [
            ['Métrica', 'Valor'],
            ['Total de pruebas', str(total)],
            ['Pruebas exitosas', str(passed)],
            ['Pruebas fallidas', str(total - passed)],
            ['Tasa de éxito', f"{(passed/total)*100:.1f}%" if total > 0 else "0%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Resultado final
        story.append(Paragraph("RESULTADO", heading_style))
        story.append(Spacer(1, 10))
        
        if passed == total:
            result_text = "✅ EXCELENTE: TODAS LAS PRUEBAS PASARON"
            result_color = colors.green
        else:
            result_text = f"⚠️ PARCIAL: {passed}/{total} PRUEBAS PASARON"
            result_color = colors.orange
        
        result_style = ParagraphStyle(
            'ResultStyle',
            parent=normal_style,
            fontSize=14,
            alignment=TA_CENTER,
            textColor=result_color,
            spaceAfter=20
        )
        
        story.append(Paragraph(result_text, result_style))
        story.append(Spacer(1, 20))
        
        # Recomendaciones
        story.append(Paragraph("RECOMENDACIONES", heading_style))
        story.append(Spacer(1, 10))
        
        if passed == total:
            recommendations = [
                "• El servicio está listo para despliegue de producción,",
                "• Todas las pruebas pasaron exitosamente,",
                "• La configuración está correcta,",
                "• Se puede proceder con el despliegue,",
                "• Monitorear el rendimiento en producción"
            ]
        else:
            recommendations = [
                "• Revisar las pruebas fallidas identificadas,",
                "• Corregir los problemas antes del despliegue,",
                "• Ejecutar las pruebas nuevamente,",
                "• Verificar la configuración del entorno,",
                "• Consultar los logs para más detalles"
            ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, normal_style))
        
        # Pie de página
        story.append(Spacer(1, 30))
        story.append(Paragraph("Reporte generado automáticamente por el sistema de pruebas", 
                              ParagraphStyle('Footer', parent=normal_style, alignment=TA_CENTER, fontSize=8)))
        
        # Generar PDF
        doc.build(story)
        
        print(f"📄 Reporte PDF generado: {filepath}")
        return filepath
        
    except ImportError:
        print("⚠️ ReportLab no está instalado. Instala con: pip install reportlab")
        return None
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        return None

async def run_tests_and_generate_report():
    """
    Ejecutar pruebas y generar reporte PDF.
    """
    print("🚀 Ejecutando pruebas de despliegue y generando reporte PDF...")
    print("=" * 60)
    
    # Importar las funciones de test desde test_deployment.py
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../..'))
    
    # Importar las funciones de test
    from scripts.deployment.test_deployment import (
        test_environment_variables,
        test_imports,
        test_configuration,
        test_database_connection,
        test_cloudinary_service,
        test_api_structure
    )
    
    tests = [
        ("Variables de entorno", test_environment_variables),
        ("Imports de módulos", test_imports),
        ("Configuración", test_configuration),
        ("Conexión MongoDB", test_database_connection),
        ("Servicio Cloudinary", test_cloudinary_service),
        ("Estructura API", test_api_structure)
    ]
    
    passed = 0
    total = len(tests)
    test_results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20}[{test_name}] {'='*20}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                await test_func()
            else:
                test_func()
            passed += 1
            print(f"✅ {test_name}: PASÓ")
            test_results[test_name] = {
                'status': 'PASÓ',
                'details': 'Prueba completada exitosamente'
            }
        except Exception as e:
            print(f"❌ {test_name}: FALLÓ - {str(e)}")
            test_results[test_name] = {
                'status': 'FALLÓ',
                'details': str(e)
            }
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    # Generar PDF
    pdf_path = generate_pdf_report(test_results, passed, total)
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El servicio está listo para despliegue.")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores antes del despliegue.")
        return False

def main():
    """
    Función principal.
    """
    try:
        success = asyncio.run(run_tests_and_generate_report())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Generación de reporte interrumpida")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 