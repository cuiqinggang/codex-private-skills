"""Local mixed-reader adapter: installed PyMuPDF for PDF, installed MarkItDown otherwise."""
import argparse,json,pathlib,zipfile
p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('files',nargs='+');a=p.parse_args()
root=pathlib.Path(a.root).resolve(strict=True);paths=[pathlib.Path(x).resolve(strict=True) for x in a.files]
for path in paths:
    if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size>64*1024*1024:raise ValueError('Input outside bounded authorized local root')
    if path.suffix.lower() in {'.docx','.xlsx','.pptx'}:
        with zipfile.ZipFile(path) as z:
            if len(z.infolist())>10000 or sum(x.file_size for x in z.infolist())>128*1024*1024:raise ValueError('Office archive exceeds bounds')
            if any('..' in pathlib.PurePosixPath(x.filename).parts or x.filename.startswith(('/','\\')) for x in z.infolist()):raise ValueError('Unsafe Office path')
engine=None;result=[]
for path in paths:
    if path.suffix.lower()=='.pdf':
        import fitz
        with fitz.open(path) as doc:text='\n\n'.join(page.get_text() for page in doc)
        route='installed PyMuPDF; no new dependencies'
    else:
        if engine is None:
            from markitdown import MarkItDown
            engine=MarkItDown(enable_plugins=False)
        text=engine.convert_local(str(path)).text_content;route='existing Microsoft MarkItDown; plugins and LLM disabled'
    result.append({'source':str(path),'markdown':text,'route':route})
print(json.dumps(result[0] if len(result)==1 else result,ensure_ascii=True))

