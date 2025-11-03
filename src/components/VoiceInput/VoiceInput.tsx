import { useState, useRef } from 'react';
import { getApiConfig } from '../../utils/config';

interface VoiceInputProps {
  onResult: (text: string) => void;
}

export default function VoiceInput({ onResult }: VoiceInputProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [status, setStatus] = useState('');
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await processAudio(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setStatus('正在录音...');
    } catch (error) {
      console.error('启动录音失败:', error);
      setStatus('无法访问麦克风');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setStatus('正在处理...');
    }
  };

  const processAudio = async (audioBlob: Blob) => {
    const config = getApiConfig('xunfei');
    if (!config) {
      setStatus('请先配置科大讯飞API');
      return;
    }

    try {
      setStatus('正在识别...');
      const { VoiceService } = await import('../../services/api');
      const voiceService = new VoiceService();
      const text = await voiceService.recognize(audioBlob);
      setStatus('识别完成');
      onResult(text);
    } catch (error: any) {
      console.error('语音识别失败:', error);
      setStatus(`识别失败: ${error.message || '请重试'}`);
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className={`px-4 py-2 rounded-lg transition-colors ${
          isRecording
            ? 'bg-red-500 text-white hover:bg-red-600'
            : 'bg-primary-600 text-white hover:bg-primary-700'
        }`}
      >
        {isRecording ? '停止录音' : '开始录音'}
      </button>
      {status && (
        <span className={`text-sm ${
          status.includes('失败') || status.includes('无法') 
            ? 'text-red-600' 
            : 'text-gray-600'
        }`}>
          {status}
        </span>
      )}
    </div>
  );
}

