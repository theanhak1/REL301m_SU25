Run gendata.ipynb để sử dụng Gemini API gen caption từ ảnh --> các file vehicle_caption_dataset.json 
Chuyển về đúng định dạng training của Qwen VL (tập train ) --> data_full.json (chạy file Data_full.py)
Chuyển về định dạng DPO --> rejected_dataset_dpo.json
Run file train_moi_nhat.ipynb để finetune mô hình Qwen 
Các trọng số đã được lưu thành các folder: dpo-qwen2-vl-checkpoint-epoch0, dpo-qwen2-vl-checkpoint-epoch1, dpo-qwen2-vl-checkpoint-epoch2
Test với mô hình Qwen gốc : run infer_model_gốc.ipynb
Test với mô hình Qwen đã finetune: run Finetune and infer.ipynb