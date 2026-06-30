import { useToast as useToastFromContext } from '../components/Toast';

export const useToast = () => {
  return useToastFromContext();
};
